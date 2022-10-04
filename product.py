from decimal import Decimal

import wx

import config as cfg
from helped import MyDialog, InterfaceListModel, InterfaceListView
import Language.en as lang

import main_container


class Detail:
    def __init__(self):
        self.__ID = wx.NewIdRef()
        self.title = None
        self.__count = None
        self.operation = None
        self.__cost = None

    @property
    def id(self) -> int:
        return self.__ID

    @property
    def count(self) -> Decimal:
        return self.__count

    @count.setter
    def count(self, count: str):
        self.__count = Decimal(count)

    @property
    def cost(self) -> Decimal:
        return self.__cost

    @cost.setter
    def cost(self, cost: str):
        self.__cost = Decimal(cost)

    def __str__(self):
        return f'{self.title}_{self.__ID.GetId()}'

    def __repr__(self):
        return self.__str__()


class Product:
    def __init__(self):
        self.__ID = wx.NewIdRef()
        self.model = None
        self.size = None
        self.__details = {}

    @property
    def id(self) -> int:
        return self.__ID.GetId()

    def __str__(self):
        return f'{self.model} [{self.size}]'

    def __repr__(self):
        return f'{self.model}_{self.size}_{self.id}'

    def add(self, detail: Detail):
        """Додає Detail в словник [Detail.id: Detail]"""
        self.__details.setdefault(detail.id, detail)

    def get(self, detail_id: int) -> Detail:
        """Повертає Detail зі словника"""
        return self.__details.get(detail_id)

    def delete(self, detail_id: int):
        """Видаляє Detail зі словника"""
        del self.__details[detail_id]

    def get_long(self) -> int:
        """Повертає довжину словника details"""
        return len(self.__details)


class TabModel(InterfaceListModel):
    def __init__(self):
        super().__init__()
        self.product: Product = None

    def __getattribute__(self, item):
        if item in ['get_name_list', 'add_in_objects', 'add_in_ids', 'del_object', 'del_id', 'objects', 'ids']:
            raise AttributeError
        else:
            return super().__getattribute__(item)

    def set_product(self, product: Product):
        """Встановлює Product"""
        self.product = product

    @staticmethod
    def create(title: str, count: str, operation: str, cost: str):
        """Повертає створений Detail."""
        detail = Detail()
        detail.title = title
        detail.count = count
        detail.operation = operation
        detail.cost = cost
        return detail

    def get_object(self, select_id: int) -> Detail:
        """Повертає Detail за індексом."""
        return self.product.get(select_id)

    def get_name(self, select_id: int) -> str:
        """Повертає ім'я за індексом"""
        return self.product.get(select_id).title

    def get_id(self, select_name: str) -> int | str:
        """Повертає індекс за ім'ям."""
        pass

    def add(self, detail: Detail):
        """Додає Detail у словники:
        details[id: detail]
        """
        self.product.add(detail)

    def delete(self, select_id: int):
        """Видаляє Detail зі словника."""
        self.product.delete(select_id)

    def set_value_widgets(self, select_id: int, title: wx.TextCtrl, count: wx.TextCtrl, operation: wx.TextCtrl, cost: wx.TextCtrl):
        """Встановлює у wx_widgets значення атрибутів Detail."""
        detail = self.get_object(select_id)
        title.SetValue(detail.title)
        count.SetValue(str(detail.count))
        operation.SetValue(detail.operation)
        cost.SetValue(str(detail.cost))

    def set_attr_select_object(self, select_id: int, title: str, count: str, operation: str, cost: str):
        """Встановлює в атрибути Detail нове значення."""
        detail = self.get_object(select_id)
        detail.title = title
        detail.count = count
        detail.operation = operation
        detail.cost = cost

    def is_long_objects_equal_one(self) -> bool:
        if self.product.get_long() == 1:
            return True
        return False

    def is_empty_objects(self) -> bool:
        if self.product.get_long() <= 0:
            return True
        return False


class ListModel(InterfaceListModel):
    def __init__(self):
        super().__init__()
        self.objects = main_container.product

    @staticmethod
    def create(model: str, size: str) -> Product:
        """Повертає створений Product."""
        product = Product()
        product.model = model
        product.size = size
        return product

    def get_object(self, select_id: int) -> Product | str:
        return super().get_object(select_id)

    def get_name(self, select_id: int):
        """Повертає ім'я за індексом"""
        return self.get_object(select_id).__str__()

    def add(self, product: Product):
        """Додає Product у словники:
        objects[id: object]
        ids[name: id]
        """
        self.add_in_objects(product.id, product)
        self.add_in_ids(product.__str__(), product.id)

    def set_value_widgets(self, select_id: int, model: wx.TextCtrl, size: wx.TextCtrl):
        """Встановлює у wx_widgets значення атрибутів Product."""
        product = self.get_object(select_id)
        model.SetValue(product.model)
        size.SetValue(product.size)

    def set_attr_select_object(self, select_id: int, model: str, size: str):
        """Змінює ім'я в словнику ids вибраного Product."""
        product = self.get_object(select_id)
        print(product)  # todo
        print(model)
        print(size)
        product.model = model
        product.size = size


class DetailView(MyDialog):
    def __init__(self, parent, model: TabModel, list_ctrl: wx.ListCtrl, select_id: int, editing: bool):
        super().__init__(parent, size=(375, 265))
        # Variables
        self.model = model
        self.list_ctrl = list_ctrl
        self.select_item = select_id
        self.editing = editing

        # Widgets
        self.st_title = wx.StaticText(self, label=lang.NAME_ST['title'])
        self.st_count_details = wx.StaticText(self, label=lang.NAME_ST['count'])
        self.st_operation = wx.StaticText(self, label=lang.NAME_ST['operation'])
        self.st_cost = wx.StaticText(self, label=lang.NAME_ST['cost'])
        self.tc_title = wx.TextCtrl(self, size=(220, -1))
        self.tc_count_details = wx.TextCtrl(self, size=(60, -1))
        self.tc_operation = wx.TextCtrl(self, size=(220, -1))
        self.tc_cost = wx.TextCtrl(self, size=(60, -1))
        self.btn_save = wx.Button(self, label=lang.NAME_BTN['save'])

        # Sizers
        form_box = wx.GridBagSizer(10, 10)
        form_box.Add(self.st_title, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.st_count_details, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.st_operation, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.st_cost, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.tc_title, pos=(0, 1))
        form_box.Add(self.tc_count_details, pos=(1, 1))
        form_box.Add(self.tc_operation, pos=(2, 1))
        form_box.Add(self.tc_cost, pos=(3, 1))
        form_box.Add(self.btn_save, pos=(4, 0), span=(1, 2), flag=wx.ALIGN_RIGHT)

        main_box = wx.BoxSizer()
        main_box.Add(form_box, flag=wx.ALL, border=10)

        self.SetSizer(main_box)

        # Binds
        self.Bind(wx.EVT_BUTTON, self.on_save, self.btn_save)

    def on_save(self, event):
        if self.editing:
            pass
        else:
            pass
        self.Destroy()


class ProductView(MyDialog):
    def __init__(self, parent, list_model: ListModel, tab_model: TabModel, list_select_id: int, list_select_name: str, list_editing: bool):
        super().__init__(parent, size=(540, 460))
        # Variable
        self.parent = parent
        self.list_model = list_model
        self.tab_model = tab_model
        self.list_select_id = list_select_id
        self.list_select_name = list_select_name
        self.list_editing = list_editing
        self.select_id = None
        self.select_name = None
        self.editing = False

        # Widgets
        self.st_model = wx.StaticText(self, label=lang.NAME_ST['model'])
        self.st_size = wx.StaticText(self, label=lang.NAME_ST['size'])
        self.st_full_cost = wx.StaticText(self, label=lang.NAME_ST['cost'])
        self.st_full_cost_value = wx.StaticText(self)
        self.st_details = wx.StaticText(self, label=lang.NAME_ST['details'])
        self.tc_model = wx.TextCtrl(self, value=lang.NAME_EXAMPLE['model'], size=(220, -1))
        self.tc_size = wx.TextCtrl(self, value=lang.NAME_EXAMPLE['size'], size=(90, -1))
        self.btn_save = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['save'])
        self.btn_add = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['add'])
        self.btn_edit = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['edit'])
        self.btn_delete = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['del'])
        self.btn_edit.Enable(False)
        self.btn_delete.Enable(False)

        self.lc_details = wx.ListCtrl(self, size=(500, 200), style=wx.LC_REPORT)
        self.lc_details.SetFont(wx.Font(wx.FontInfo(12)))
        self.lc_details.InsertColumn(0, heading=lang.NAME_COL_HEADER['title'], width=150)
        self.lc_details.InsertColumn(1, heading=lang.NAME_COL_HEADER['id'], width=0)
        self.lc_details.InsertColumn(2, heading=lang.NAME_COL_HEADER['count'], width=60)
        self.lc_details.InsertColumn(3, heading=lang.NAME_COL_HEADER['operation'], width=150)
        self.lc_details.InsertColumn(4, heading=lang.NAME_COL_HEADER['cost'], width=60)

        # Sizers
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_box.Add(self.btn_save, flag=wx.RIGHT, border=10)
        btn_box.Add(self.btn_add, flag=wx.RIGHT, border=10)
        btn_box.Add(self.btn_edit, flag=wx.RIGHT, border=10)
        btn_box.Add(self.btn_delete)

        form_box = wx.GridBagSizer(10, 10)
        form_box.Add(self.st_model, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.tc_model, pos=(0, 1))
        form_box.Add(self.st_size, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.tc_size, pos=(1, 1))
        form_box.Add(self.st_full_cost, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        form_box.Add(self.st_full_cost_value, pos=(2, 1))
        form_box.Add(self.st_details, pos=(3, 0))
        form_box.Add(self.lc_details, pos=(4, 0), span=(1, 2))
        form_box.Add(btn_box, pos=(5, 0), span=(1, 2))

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(form_box, flag=wx.ALL, border=10)

        self.SetSizer(main_box)

        # Binds
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.btn_save)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.on_edit, self.btn_edit)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.btn_delete)

        # Methods

    def on_select(self, event):
        pass

    def on_save(self, event):
        if self.list_editing:
            self.list_model.set_attr_select_object(self.list_select_id, *self.get_all_value_widgets())
            self.list_model.change_name_select_object(self.list_select_id, self.list_select_name)
        else:
            self.tab_model.product.model = self.tc_model.GetValue()
            self.tab_model.product.size = self.tc_size.GetValue()
            self.list_model.add(self.tab_model.product)
        self.Destroy()

    def on_add(self, event):
        pass

    def on_edit(self, event):
        pass

    def on_delete(self, event):
        pass

    def get_all_widgets(self) -> tuple:
        return self.tc_model, self.tc_size

    def get_all_value_widgets(self) -> tuple:
        return self.tc_model.GetValue(), self.tc_size.GetValue()


class ProductListView(InterfaceListView):
    def __init__(self, parent, list_model: ListModel, tab_model: TabModel):
        super().__init__(parent, list_model)
        self.tab_model = tab_model

    def show_default_object_view(self):
        """Показує діалогове вікно Product заповнене за замовчуванням"""
        self.tab_model.product = Product()
        laborer_view = ProductView(self.parent, self.model, self.tab_model, self.select_id, self.select_name, self.editing)
        laborer_view.ShowModal()

    def show_fulled_object_view(self):
        """Показує діалогове вікно заповнене атрибутами вибраного Product."""
        self.tab_model.product = self.model.get_object(self.select_id)
        laborer_view = ProductView(self.parent, self.model, self.tab_model, self.select_id, self.select_name, self.editing)
        self.model.set_value_widgets(self.select_id, *laborer_view.get_all_widgets())
        laborer_view.ShowModal()

    def show_info_view(self):
        """Показує діалогове вікно заповнене інформацією вибраного Product."""
        ProductView(self.parent, self.model.get_object(self.select_id)).ShowModal()
