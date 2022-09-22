from decimal import Decimal

import wx

import config as cfg
from helped import MyDialog, InterfaceListModel, InterfaceListView
import Language.en as lang

import main_container


class Laborer:
    def __init__(self, full_name: str = None,
                 job_title: str = None,
                 payment: str = None,
                 rate: Decimal = None):
        self.full_name = full_name
        self.job_title = job_title
        self.payment = payment
        self.rate = Decimal(rate) if rate is not None else rate

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.__str__()


class ListModel(InterfaceListModel):
    def __init__(self):
        super().__init__()
        self.object_dict = main_container.laborer

    def edit(self, select: str, **kwargs):
        super().edit(select, **kwargs)
        self.object_dict[select].rate = Decimal(self.object_dict[select].rate)


class InfoView(MyDialog):
    def __init__(self, parent, laborer: Laborer, *args, **kwargs):
        super().__init__(parent, size=(350, 200), *args, **kwargs)

        st_full_name = wx.StaticText(self, label=f'{lang.NAME_ST["full_name"]} {laborer.full_name}')
        st_job_title = wx.StaticText(self, label=f'{lang.NAME_ST["job_title"]} {laborer.job_title}')
        st_payment = wx.StaticText(self, label=f'{lang.NAME_ST["payment"]} {laborer.payment}')
        rate_label = f'{lang.NAME_ST["rate"]} {laborer.rate}' if laborer.payment == lang.NAME_CB['payment'][1] else ''
        st_rate = wx.StaticText(self, label=rate_label)

        mani_box = wx.BoxSizer(wx.VERTICAL)
        mani_box.Add(st_full_name, flag=wx.ALL, border=10)
        mani_box.Add(st_job_title, flag=wx.LEFT | wx.BOTTOM, border=10)
        mani_box.Add(st_payment, flag=wx.LEFT | wx.BOTTOM, border=10)
        mani_box.Add(st_rate, flag=wx.LEFT, border=10)
        self.SetSizer(mani_box)


class ProfileView(MyDialog):
    def __init__(self, parent, model: ListModel, select: str, editing: bool, *args, **kwargs):
        super().__init__(parent, size=(380, 300), *args, **kwargs)
        self.model = model
        self.select = select
        self.editing = editing

        st_full_name = wx.StaticText(self, label=lang.NAME_ST['full_name'])
        st_job_title = wx.StaticText(self, label=lang.NAME_ST['job_title'])
        st_payment = wx.StaticText(self, label=lang.NAME_ST['payment'])
        st_rate = wx.StaticText(self, label=lang.NAME_ST['rate'])
        self.tc_full_name = wx.TextCtrl(self, value='Julia J. J.', size=(220, -1))
        self.cb_job_title = wx.ComboBox(self, value=main_container.job_title[0], size=(220, -1), choices=main_container.job_title,
                                        style=wx.CB_READONLY)
        self.cb_payment = wx.ComboBox(self, value=lang.NAME_CB['payment'][0], choices=lang.NAME_CB['payment'], style=wx.CB_READONLY)
        self.tc_rate = wx.TextCtrl(self, value='0')
        self.tc_rate.Enable(False)
        self.btn_save = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['save'])

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

        self.Bind(wx.EVT_BUTTON, self.on_save, self.btn_save)
        self.Bind(wx.EVT_COMBOBOX, self.on_payment)

    def on_payment(self, event):
        if self.cb_payment.GetValue() == lang.NAME_CB['payment'][0]:
            self.tc_rate.Enable(False)
        else:
            self.tc_rate.Enable(True)

    def on_save(self, event):
        if self.editing:
            self.model.edit(self.select, full_name=self.tc_full_name,
                            job_title=self.cb_job_title,
                            payment=self.cb_payment,
                            rate=self.tc_rate)
        else:
            laborer = Laborer(self.tc_full_name.GetValue(),
                              self.cb_job_title.GetValue(),
                              self.cb_payment.GetValue(),
                              self.tc_rate.GetValue())
            self.model.add(laborer)
        self.Destroy()


class ListView(InterfaceListView):
    def __init__(self, parent, model):
        super().__init__(parent, model, title=lang.NAME_TITLE['laborer'])

    def on_info(self, event):
        super().on_info(InfoView)

    def on_add(self, event):
        super().on_add(ProfileView)

    def on_edit(self, event):
        self.editing = True
        profile_view = ProfileView(self.parent, self.model, self.select, self.editing)
        self.model.set(self.select, full_name=profile_view.tc_full_name,
                       job_title=profile_view.cb_job_title,
                       payment=profile_view.cb_payment,
                       rate=profile_view.tc_rate)
        profile_view.on_payment('event')
        profile_view.ShowModal()
        self.list_box.SetItems(self.model.name_list)
