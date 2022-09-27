from decimal import Decimal

import wx

import config as cfg
from helped import MyDialog, InterfaceListModel, InterfaceListView, MyPanel, print_indicator
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


class ListModel:
    def __init__(self):
        self.laborers: dict[int: Laborer] = main_container.laborer
        self.ids: dict[str: int] = {}

    @staticmethod
    def create(full_name: str, job_title: str, payment: str, rate: str) -> Laborer:
        """Повертає створений Laborer."""
        laborer = Laborer()
        laborer.full_name = full_name
        laborer.job_title = job_title
        laborer.payment = payment
        laborer.rate = rate
        return laborer

    def get_name_list(self) -> list[str]:
        """Повертає список імен Laborer.full_name."""
        return [*self.ids.keys()]

    def get_laborer(self, select_id: int) -> Laborer:
        """Повертає Laborer за індексом."""
        return self.laborers.get(select_id, 'None ID')

    def get_name(self, select_id: int) -> str:
        """Повертає ім'я за індексом"""
        return self.get_laborer(select_id).full_name

    def get_id(self, select_name: str) -> int:
        """Повертає індекс за ім'ям."""
        return self.ids.get(select_name, 'None Name')

    def add(self, laborer: Laborer):
        """Додає Laborer у словники:
        laborers[Laborer.id: Laborer]
        names[Laborer.id: Laborer.full_name]
        """
        self.__add_in_laborers(laborer)
        self.__add_in_ids(laborer)

    def delete(self, select_id: int, select_name: str):
        """Видаляє Laborer та його атрибути з усіх словників"""
        self.__del_laborer(select_id)
        self.__del_id(select_name)

    def set_attrs_select_laborer(self, select_id: int, full_name: str, job_title: str, payment: str, rate: str):
        """Встановлює атрибути вибраного Laborer"""
        laborer = self.get_laborer(select_id)
        laborer.full_name = full_name
        laborer.job_title = job_title
        laborer.payment = payment
        laborer.rate = rate

    def change_name_select_laborer(self, select_id: int, select_name: str):
        """Змінює ім'я в словнику ids вибраного Laborer."""
        old_name = select_name
        new_name = self.get_name(select_id)
        if old_name != new_name:
            self.__del_id(select_name)
            self.__add_in_ids(self.get_laborer(select_id))

    def set_value_widgets(self, select_id: int, full_name: wx.TextCtrl, job_title: wx.ComboBox, payment: wx.ComboBox, rate: wx.TextCtrl):
        """Встановлює у wx_widgets значення атрибутів Laborer."""
        laborer = self.get_laborer(select_id)
        full_name.SetValue(laborer.full_name)
        job_title.SetValue(laborer.job_title)
        payment.SetValue(laborer.payment)
        rate.SetValue(str(laborer.rate))

    def is_long_laborers_equal_one(self) -> bool:
        if len(self.laborers) == 1:
            return True
        return False

    def is_empty_laborers(self) -> bool:
        if len(self.laborers) <= 0:
            return True
        return False

    def __add_in_laborers(self, laborer: Laborer):
        self.laborers.setdefault(laborer.id, laborer)

    def __add_in_ids(self, laborer: Laborer):
        self.ids.setdefault(laborer.full_name, laborer.id)

    def __del_laborer(self, select_id: int):
        del self.laborers[select_id]

    def __del_id(self, select_name: str):
        del self.ids[select_name]


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
            self.model.change_name_select_laborer(self.select_id, self.select_name)
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


class LaborerListView(MyPanel):
    def __init__(self, parent, model: ListModel):
        super().__init__(parent)
        # Variables
        self.parent = parent
        self.select_id = None
        self.select_name = None
        self.editing = False
        self.model = model

        # Widgets
        st_title = wx.StaticText(self, label=lang.NAME_TITLE['laborer'])
        self.list_box = wx.ListBox(self, size=(210, 270), choices=self.model.get_name_list())
        self.btn_info = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['info'])
        self.btn_add = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['add'])
        self.btn_edit = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['edit'])
        self.btn_del = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['del'])

        # Sizers
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(st_title, flag=wx.ALIGN_CENTRE | wx.TOP | wx.BOTTOM, border=10)
        main_box.Add(self.list_box, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_info, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_add, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_edit, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_del, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)

        self.SetSizer(main_box)

        # Binds
        self.Bind(wx.EVT_BUTTON, self.on_info, self.btn_info)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.btn_del)
        self.Bind(wx.EVT_BUTTON, self.on_edit, self.btn_edit)
        self.Bind(wx.EVT_LISTBOX, self.on_select)

        # Methods
        self.disable_buttons()

    def on_select(self, event):
        index = self.list_box.GetSelection()
        self.select_name = self.model.get_name_list()[index]
        self.select_id = self.model.get_id(self.select_name)

    def on_info(self, event):
        if self.select_id is not None:
            laborer = self.model.get_laborer(self.select_id)
            LaborerInfoView(self.parent, laborer).ShowModal()

    def on_add(self, event):
        self.editing = False
        self.show_default_laborer_view()
        self.fulled_list()
        self.enable_buttons()

    def on_edit(self, event):
        if self.select_id is not None:
            self.editing = True
            self.show_default_laborer_view()
            self.fulled_list()

    def on_delete(self, event):
        if self.select_id is not None:
            self.model.delete(self.select_id, self.select_name)
            self.select_id = None
            self.select_name = None
            self.fulled_list()
            self.disable_buttons()

    def fulled_list(self):
        """Заповнює list_box"""
        self.list_box.SetItems(self.model.get_name_list())

    def enable_buttons(self):
        """Вмикає кнопки info, edit та del якщо в laborers є 1 елемент."""
        if self.model.is_long_laborers_equal_one():
            self.btn_info.Enable(True)
            self.btn_edit.Enable(True)
            self.btn_del.Enable(True)

    def disable_buttons(self):
        """Вимикає кнопки info, edit та del якщо laborers порожній."""
        if self.model.is_empty_laborers():
            self.btn_info.Enable(False)
            self.btn_edit.Enable(False)
            self.btn_del.Enable(False)

    def show_default_laborer_view(self):
        """Показує діалогове вікно заповнене за замовчуванням"""
        laborer_view = LaborerView(self.parent, self.model, self.select_id, self.select_name, self.editing)
        laborer_view.ShowModal()

    def show_fulled_laborer_view(self):
        """Показує діалогове вікно заповнене атрибутами вибраного Laborer."""
        laborer_view = LaborerView(self.parent, self.model, self.select_id, self.select_name, self.editing)
        self.model.set_value_widgets(self.select_id, *laborer_view.get_all_widgets())
        laborer_view.enable_tc_rate()
        laborer_view.ShowModal()
