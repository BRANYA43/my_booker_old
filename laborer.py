from decimal import Decimal

import wx

import config as cfg
from helped import MyDialog, InterfaceListModel, InterfaceListView, MyPanel
import Language.en as lang

import main_container


class Laborer:
    def __init__(self):
        self.__ID = wx.NewIdRef()
        self.full_name = None
        self.job_title = None
        self.payment = None
        self.__rate = None

    @property
    def id(self) -> int:
        return self.__ID.GetId()

    @property
    def rate(self) -> Decimal:
        return self.__rate

    @rate.setter
    def rate(self, rate: str):
        self.__rate = Decimal(rate)

    def __str__(self):
        return f'{self.full_name}_{self.id}'

    def __repr__(self):
        return self.__str__()


class ListModel(InterfaceListModel):
    def __init__(self):
        super().__init__()
        self.objects: dict[int: Laborer] = main_container.laborer

    @staticmethod
    def create(full_name: str, job_title: str, payment: str, rate: str) -> Laborer:
        """Повертає створений Laborer."""
        laborer = Laborer()
        laborer.full_name = full_name
        laborer.job_title = job_title
        laborer.payment = payment
        laborer.rate = rate
        return laborer

    def get_name(self, select_id: int) -> str:
        """Повертає ім'я за індексом"""
        return self.get_object(select_id).full_name

    def add(self, laborer: Laborer):
        """Додає Object у словники:
        objects[id: object]
        ids[name: id]
        """
        self.add_in_objects(laborer.id, laborer)
        self.add_in_ids(laborer.full_name, laborer.id)

    def set_value_widgets(self, select_id: int, full_name: wx.TextCtrl, job_title: wx.ComboBox, payment: wx.ComboBox, rate: wx.TextCtrl):
        """Встановлює у wx_widgets значення атрибутів Object."""
        laborer = self.get_object(select_id)
        full_name.SetValue(laborer.full_name)
        job_title.SetValue(laborer.job_title)
        payment.SetValue(laborer.payment)
        rate.SetValue(str(laborer.rate))

    def set_attrs_select_laborer(self, select_id: int, full_name: str, job_title: str, payment: str, rate: str):
        """Встановлює атрибути вибраного Object"""
        laborer = self.get_object(select_id)
        laborer.full_name = full_name
        laborer.job_title = job_title
        laborer.payment = payment
        laborer.rate = rate


class LaborerInfoView(MyDialog):
    def __init__(self, parent, laborer: Laborer):
        super().__init__(parent, size=(350, 200))

        # Widgets
        st_full_name = wx.StaticText(self, label=f'{lang.NAME_ST["full_name"]} {laborer.full_name}')
        st_job_title = wx.StaticText(self, label=f'{lang.NAME_ST["job_title"]} {laborer.job_title}')
        st_payment = wx.StaticText(self, label=f'{lang.NAME_ST["payment"]} {laborer.payment}')
        rate_label = f'{lang.NAME_ST["rate"]} {laborer.rate}' if laborer.payment == lang.NAME_CB['payment'][1] else ''
        st_rate = wx.StaticText(self, label=rate_label)

        # Sizers
        mani_box = wx.BoxSizer(wx.VERTICAL)
        mani_box.Add(st_full_name, flag=wx.ALL, border=10)
        mani_box.Add(st_job_title, flag=wx.LEFT | wx.BOTTOM, border=10)
        mani_box.Add(st_payment, flag=wx.LEFT | wx.BOTTOM, border=10)
        mani_box.Add(st_rate, flag=wx.LEFT, border=10)
        self.SetSizer(mani_box)


class LaborerView(MyDialog):
    def __init__(self, parent, model: ListModel, select_id: int, select_name: str, editing: bool):
        super().__init__(parent, size=(380, 300))
        # Variables
        self.model = model
        self.select_id = select_id
        self.select_name = select_name
        self.editing = editing

        # Widgets
        st_full_name = wx.StaticText(self, label=lang.NAME_ST['full_name'])
        st_job_title = wx.StaticText(self, label=lang.NAME_ST['job_title'])
        st_payment = wx.StaticText(self, label=lang.NAME_ST['payment'])
        st_rate = wx.StaticText(self, label=lang.NAME_ST['rate'])
        self.tc_full_name = wx.TextCtrl(self, value=lang.NAME_EXAMPLE['full_name'], size=(220, -1))
        self.cb_job_title = wx.ComboBox(self, value=main_container.job_title[0], size=(220, -1), choices=main_container.job_title,
                                        style=wx.CB_READONLY)
        self.cb_payment = wx.ComboBox(self, value=lang.NAME_CB['payment'][0], choices=lang.NAME_CB['payment'], style=wx.CB_READONLY)
        self.tc_rate = wx.TextCtrl(self, value='0')
        self.tc_rate.Enable(False)
        self.btn_save = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['save'])

        # Sizers
        profile_box = wx.GridBagSizer(10, 10)
        profile_box.Add(st_full_name, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        profile_box.Add(self.tc_full_name, pos=(0, 1))
        profile_box.Add(st_job_title, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        profile_box.Add(self.cb_job_title, pos=(1, 1))
        profile_box.Add(st_payment, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        profile_box.Add(self.cb_payment, pos=(2, 1))
        profile_box.Add(st_rate, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        profile_box.Add(self.tc_rate, pos=(3, 1))
        profile_box.Add(self.btn_save, pos=(5, 1), span=(1, 2), flag=wx.ALIGN_RIGHT)

        main_box = wx.BoxSizer()
        main_box.Add(profile_box, flag=wx.ALL, border=10)

        self.SetSizer(main_box)

        # Binds
        self.Bind(wx.EVT_BUTTON, self.on_save, self.btn_save)
        self.Bind(wx.EVT_COMBOBOX, self.on_payment)

    def on_payment(self, event):
        self.enable_tc_rate()

    def on_save(self, event):
        if self.editing:
            self.model.set_attrs_select_laborer(self.select_id, *self.__get_all_value_widgets())
            self.model.change_name_select_object(self.select_id, self.select_name)
        else:
            laborer = self.model.create(*self.__get_all_value_widgets())
            self.model.add(laborer)
        self.Destroy()

    def enable_tc_rate(self):
        if self.cb_payment.GetValue() == lang.NAME_CB['payment'][0]:
            self.tc_rate.Enable(False)
        else:
            self.tc_rate.Enable(True)

    def get_all_widgets(self) -> tuple:
        return self.tc_full_name, self.cb_job_title, self.cb_payment, self.tc_rate

    def __get_all_value_widgets(self) -> tuple:
        return self.tc_full_name.GetValue(), self.cb_job_title.GetValue(), self.cb_payment.GetValue(), self.tc_rate.GetValue()


class LaborerListView(InterfaceListView):
    def __init__(self, parent, model: ListModel):
        super().__init__(parent, model)

    def show_default_object_view(self):
        """Показує діалогове вікно Object заповнене за замовчуванням"""
        laborer_view = LaborerView(self.parent, self.model, self.select_id, self.select_name, self.editing)
        laborer_view.ShowModal()

    def show_fulled_object_view(self):
        """Показує діалогове вікно заповнене атрибутами вибраного Object."""
        laborer_view = LaborerView(self.parent, self.model, self.select_id, self.select_name, self.editing)
        self.model.set_value_widgets(self.select_id, *laborer_view.get_all_widgets())
        laborer_view.enable_tc_rate()
        laborer_view.ShowModal()

    def show_info_view(self):
        """Показує діалогове вікно заповнене інформацією вибраного Object."""
        LaborerInfoView(self.parent, self.model.get_object(self.select_id)).ShowModal()
