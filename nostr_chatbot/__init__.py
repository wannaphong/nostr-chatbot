import time
import uuid
import logging
from collections import defaultdict
from .nostr.key import PrivateKey,PublicKey
from .nostr.filter import Filter, Filters
from .nostr.event import Event, EventKind
from .nostr.relay_manager import RelayManager
from .nostr.message_type import ClientMessageType
from .nostr.event import EncryptedDirectMessage
from .nostr.relay_manager import RelayManager


class Chatbot:
    def __init__(
            self,
            private_key:str,
            recipient_pubkey:str,
            setup:bool=False,
            relay:list=["wss://nostr-pub.wellorder.net","wss://relay.damus.io","wss://nos.lol"]
        ) -> None:
        """
        :param str private_key: private_key (nsec)
        :param str recipient_pubkey: recipient public key (npub)
        :param bool setup: load history chat
        :param list relay: List relay
        """
        self.relay = relay
        if recipient_pubkey==None:
            self.recipient_pubkey = recipient_pubkey
        else:
            self.recipient_pubkey = PublicKey.from_npub(recipient_pubkey)
        self.private_key = PrivateKey.from_nsec(private_key)
        self.relay_manager = RelayManager()
        for i in self.relay:
            self.relay_manager.add_relay(i)
        self.subscription_id = uuid.uuid1().hex
        self.history = defaultdict(lambda: defaultdict(list))
        #{"bot":[],"recipient":[]}
        self.setup_receive()

        if setup:
            logging.info("setuping...")
            self.setup()
            logging.info("done!")
    
    def setup_receive(self):
        self.filters = Filters([
            Filter(
            kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],
            pubkey_refs=[self.private_key.public_key.hex()]
            )
        ])
        self.relay_manager2 = RelayManager()
        for i in self.relay:
            self.relay_manager2.add_relay(i)
        self.subscription_id2 = uuid.uuid1().hex
        self.relay_manager2.add_subscription_on_all_relays(self.subscription_id2, self.filters)

    def setup(self):
        """
        for get old chat (from recipient response olny)
        """
        filters2 = Filters([
            Filter(
            kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],
            authors=[self.private_key.public_key.hex()]
            )
        ])
        relay_manager3 = RelayManager()
        for i in self.relay:
            relay_manager3.add_relay(i)
        subscription_id3 = uuid.uuid1().hex
        relay_manager3.add_subscription_on_all_relays(subscription_id3, filters2)
        while relay_manager3.message_pool.has_events():
            event_msg = relay_manager3.message_pool.get_event()
            self.history[self.recipient_pubkey.bech32()]["bot"].append(event_msg.event)
        relay_manager3.close_subscription_on_all_relays(id=subscription_id3)
        while self.relay_manager2.message_pool.has_events():
            event_msg = self.relay_manager2.message_pool.get_event()
            self.history[self.recipient_pubkey.bech32()]["recipient"].append(event_msg.event)
        self.history[self.recipient_pubkey.bech32()]["bot"]=sorted(self.history[self.recipient_pubkey.bech32()]["bot"], key=lambda d: d.created_at)
        self.history[self.recipient_pubkey.bech32()]["recipient"]=sorted(self.history[self.recipient_pubkey.bech32()]["recipient"], key=lambda d: d.created_at)

    def send(self, message:str):
        """
        :param str message: message
        """
        dm = EncryptedDirectMessage(
            recipient_pubkey=self.recipient_pubkey.hex(),
            cleartext_content=message
        )
        self.private_key.sign_event(dm)
        self.relay_manager.publish_event(dm)
        self.history[self.recipient_pubkey.bech32()]["bot"].append(dm)

    def close(self):
        """
        close all subscription on all relays
        """
        self.relay_manager.close_subscription_on_all_relays(id=self.subscription_id)
        self.relay_manager2.close_subscription_on_all_relays(id=self.subscription_id2)

    def receive(self)->str:
        """
        receive a message from recipient.
        """
        while self.relay_manager2.message_pool.has_events():
            event_msg = self.relay_manager2.message_pool.get_event()
            if self.recipient_pubkey.bech32() not in self.history.keys():
                pass
            elif event_msg.event.created_at<self.history[self.recipient_pubkey.bech32()]["bot"][-1].created_at:
                return None
            self.history[self.recipient_pubkey.bech32()]["recipient"].append(event_msg.event)
        if self.history[self.recipient_pubkey.bech32()]["recipient"]==[]:
            return None
        if self.history[self.recipient_pubkey.bech32()]["recipient"][-1].created_at<self.history[self.recipient_pubkey.bech32()]["bot"][-1].created_at:
            return None
        e= self.history[self.recipient_pubkey.bech32()]["recipient"][-1]
        return self.private_key.decrypt_message(e.content,e.public_key)
