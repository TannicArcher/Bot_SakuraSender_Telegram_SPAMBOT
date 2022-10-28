from aiogram.dispatcher.filters.state import StatesGroup, State


class EditChat(StatesGroup):
    EC1 = State()


class DelAcc(StatesGroup):
    D1 = State()


class AddProxy(StatesGroup):
    P1 = State()


class DelProxy(StatesGroup):
    P1 = State()


class SpamChat(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()
    S4 = State()
    S5 = State()
    S6 = State()


class SpamUser(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()
    S4 = State()
    S5 = State()


class SpamBot(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()
    S4 = State()


class AddAccount(StatesGroup):
    A1 = State()
    A2 = State()
    A3 = State()
    A4 = State()
    A5 = State()
    A6 = State()


class AddChat(StatesGroup):
    A1 = State()
    A2 = State()


class SendMessageState(StatesGroup):
    A1 = State()
    A2 = State()


class GiveTime(StatesGroup):
    GT1 = State()
    GT2 = State()


class TakeTime(StatesGroup):
    T1 = State()
    T2 = State()


class BroadcastState(StatesGroup):
    BS1 = State()
    BS2 = State()
    BS3 = State()
    BS4 = State()
