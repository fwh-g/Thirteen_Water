import wx
import wx.grid
import json
import requests
from algorithm import *


class Start(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.init_p = None
        self.font1 = wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.font2 = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitStart()

    def OnPaintLong(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("login.png")
        dc.DrawBitmap(bmp, 0, 0)

    def InitStart(self):
        self.init_p = wx.Panel(self)
        self.init_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintLong)
        title = wx.StaticText(self.init_p, -1, '福建十三水', style=wx.ALIGN_CENTER, pos=(500, 100))
        title.SetFont(self.font1)
        lg = wx.Button(self.init_p, label='登录', pos=(585, 300), size=(70, 40))
        lg.Bind(wx.EVT_BUTTON, self.OnLogin)
        lg.SetFont(self.font2)
        rg = wx.Button(self.init_p, label='注册', pos=(585, 350), size=(70, 40))
        rg.Bind(wx.EVT_BUTTON, self.OnRegister)
        rg.SetFont(self.font2)
        ex1 = wx.Button(self.init_p, label='退出', pos=(585, 400), size=(70, 40))
        ex1.Bind(wx.EVT_BUTTON, self.OnExit)
        ex1.SetFont(self.font2)

    def OnLogin(self, event):
        self.Destroy()
        login = Login()
        login.Show()

    def OnRegister(self, event):
        self.Destroy()
        register = Register()
        register.Show()

    def OnExit(self, event):
        self.Destroy()


class Login(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.login_p = None
        self.name_in = None
        self.password_in = None
        self.font1 = wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.font2 = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitLogin()
        self.token = ''

    def OnPaintLong(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("login.png")
        dc.DrawBitmap(bmp, 0, 0)

    def InitLogin(self):
        self.login_p = wx.Panel(self)
        self.login_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintLong)
        title = wx.StaticText(self.login_p, -1, '福建十三水', style=wx.ALIGN_CENTER, pos=(500, 100))
        title.SetFont(self.font1)
        user_name = wx.StaticText(self.login_p, -1, '用户名:', style=wx.ALIGN_LEFT, pos=(500, 300))
        user_name.SetFont(self.font2)
        user_password = wx.StaticText(self.login_p, -1, '密码:', style=wx.ALIGN_LEFT, pos=(500, 350))
        user_password.SetFont(self.font2)
        self.name_in = wx.TextCtrl(self.login_p, -1, pos=(620, 300), style=wx.TE_LEFT)
        self.password_in = wx.TextCtrl(self.login_p, -1, pos=(620, 350), style=wx.TE_LEFT | wx.TE_PASSWORD)
        login = wx.Button(self.login_p, label='登录', pos=(500, 400), size=(230, 40))
        login.SetFont(self.font2)
        login.Bind(wx.EVT_BUTTON, self.OnLogin)
        back = wx.Button(self.login_p, label='返回', pos=(1100, 600))
        back.SetFont(self.font2)
        back.Bind(wx.EVT_BUTTON, self.OnBack)

    def OnBack(self, event):
        self.Destroy()
        start = Start()
        start.Show()

    def OnLogin(self, event):
        username = self.name_in.GetValue()
        password = self.password_in.GetValue()
        url = "http://api.revth.com/auth/login"
        payload = "{\"username\":\"" + str(username) + "\",\"password\":\"" + str(password) + "\"}"
        headers = {'content-type': 'application/json'}
        response = requests.request("POST", url, data=payload, headers=headers)
        dict1 = dict(response.json())
        a = dict1.get('status')
        if a == 0:
            dict2 = dict(dict1.get('data'))
            self.token = dict2.get('token')
            hall = Hall(self.token)
            self.Destroy()
            hall.Show()
        elif a == 1005:
            msg = '用户名或密码错误'
            wx.MessageBox(msg)
        else:
            msg = '登录失败'
            wx.MessageBox(msg)


class Register(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.register_p = None
        self.name_in = None
        self.password_in = None
        self.stu_number_in = None
        self.stu_password_in = None
        self.account = {'username': '', 'password': ''}
        self.jwc = {'student_number': '', 'student_password': ''}
        self.font1 = wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.font2 = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitRegister()

    def OnPaintLong(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("login.png")
        dc.DrawBitmap(bmp, 0, 0)

    def InitRegister(self):
        self.register_p = wx.Panel(self)
        self.register_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintLong)
        title = wx.StaticText(self.register_p, -1, '福建十三水', style=wx.ALIGN_CENTER, pos=(500, 100))
        title.SetFont(self.font1)
        user_name = wx.StaticText(self.register_p, -1, '用户名:', style=wx.ALIGN_LEFT, pos=(500, 250))
        user_name.SetFont(self.font2)
        user_password = wx.StaticText(self.register_p, -1, '密码:', style=wx.ALIGN_LEFT, pos=(500, 300))
        user_password.SetFont(self.font2)
        stu_number = wx.StaticText(self.register_p, -1, '学号:', style=wx.ALIGN_LEFT, pos=(500, 350))
        stu_number.SetFont(self.font2)
        stu_password = wx.StaticText(self.register_p, -1, '教务处密码:', style=wx.ALIGN_LEFT, pos=(500, 400))
        stu_password.SetFont(self.font2)
        self.name_in = wx.TextCtrl(self.register_p, -1, pos=(620, 250), style=wx.TE_LEFT)
        self.password_in = wx.TextCtrl(self.register_p, -1, pos=(620, 300), style=wx.TE_LEFT | wx.TE_PASSWORD)
        self.stu_number_in = wx.TextCtrl(self.register_p, -1, pos=(620, 350), style=wx.TE_LEFT)
        self.stu_password_in = wx.TextCtrl(self.register_p, -1, pos=(700, 400), style=wx.TE_LEFT | wx.TE_PASSWORD)
        register = wx.Button(self.register_p, label='注册', pos=(500, 460), size=(230, 40))
        register.SetFont(self.font2)
        register.Bind(wx.EVT_BUTTON, self.OnRegister)
        back = wx.Button(self.register_p, label='返回', pos=(1100, 600))
        back.SetFont(self.font2)
        back.Bind(wx.EVT_BUTTON, self.OnBack)

    def OnRegister(self, event):
        msg = ''
        username = self.name_in.GetValue()
        password = self.password_in.GetValue()
        stu_number = self.stu_number_in.GetValue()
        stu_password = self.stu_password_in.GetValue()
        self.account['username'] = username
        self.account['password'] = password
        self.jwc['student_number'] = stu_number
        self.jwc['student_password'] = stu_password
        url = "http://api.revth.com/auth/register2"
        form_data = {
            "username": self.account["username"],
            "password": self.account["password"],
            "student_number": self.jwc["student_number"],
            "student_password": self.jwc["student_password"]
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(url=url, headers=headers, data=json.dumps(form_data), verify=False)
        print(response.text)
        dict1 = dict(response.json())
        if dict1.get('status') == 0:
            msg = '注册成功'
            self.Destroy()
            start = Start()
            start.Show()
        elif dict1.get('status') == 1001:
            msg = '用户名已被使用'
        elif dict1.get('status') == 1002:
            msg = '学号已绑定'
        elif dict1.get('status') == 1003:
            msg = '教务处认证失败'
        elif dict1.get('status') == 1004:
            msg = 'Token过期'
        else:
            # msg = dict1.get('status') + str(username) + ' ' + str(password) + ' ' + str(stu_number) + ' ' + str(stu_password)
            msg = '未知错误'
        wx.MessageBox(msg)

    def OnBack(self, event):
        self.Destroy()
        start = Start()
        start.Show()


class Hall(wx.Frame):
    def __init__(self, token):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.hall_p = None
        self.token = token
        self.font = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitHall()

    def InitHall(self):
        self.hall_p = wx.Panel(self)
        self.hall_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintHall)
        begin = wx.Button(self.hall_p, label='开\n始\n游\n戏', pos=(800, 100), size=(80, 250))
        begin.Bind(wx.EVT_BUTTON, self.OnBegin)
        begin.SetFont(self.font)
        rank = wx.Button(self.hall_p, label='排\n行\n榜', pos=(900, 100), size=(80, 250))
        rank.Bind(wx.EVT_BUTTON, self.OnRank)
        rank.SetFont(self.font)
        history = wx.Button(self.hall_p, label='历\n史\n战\n况', pos=(1000, 100), size=(80, 250))
        history.Bind(wx.EVT_BUTTON, self.OnHistory)
        history.SetFont(self.font)
        all_battle = wx.Button(self.hall_p, label='对\n局\n查\n询', pos=(1100, 100), size=(80, 250))
        all_battle.Bind(wx.EVT_BUTTON, self.OnAllBattle)
        all_battle.SetFont(self.font)
        out = wx.Button(self.hall_p, label='注销', pos=(1100, 600), size=(85, 45))
        out.Bind(wx.EVT_BUTTON, self.OnOut)
        out.SetFont(self.font)

    def OnPaintHall(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("hall.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def OnOut(self, event):
        url = 'http://api.revth.com/auth/logout'
        header = {"X-Auth-Token": '\"' + str(self.token) + '\"'}
        response = requests.post(url=url, headers=header)
        dict1 = dict(response.json())
        if dict1.get('status') == 0:
            self.Destroy()
            login = Login()
            login.Show()

    def OnBegin(self, event):
        self.Destroy()
        game = Game(self.token)
        game.Show()

    def OnRank(self, event):
        self.Destroy()
        rank = Rank(self.token)
        rank.Show()

    def OnHistory(self, event):
        self.Destroy()
        history = History(self.token)
        history.Show()

    def OnAllBattle(self, event):
        self.Destroy()
        all_battle = FindBattle(self.token)
        all_battle.Show()


class Game(wx.Frame):
    def __init__(self, token):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.game_p = None
        self.go = None
        self.play = None
        self.id = None
        self.hand = None
        self.back = None
        self.token = token
        self.font = wx.Font(42, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.font2 = wx.Font(34, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitGame()

    def InitGame(self):
        self.game_p = wx.Panel(self)
        self.game_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintGame)
        self.go = wx.Button(self.game_p, label='开始', pos=(550, 320), size=(120, 70))
        self.go.Bind(wx.EVT_BUTTON, self.OnGo)
        self.go.SetFont(self.font)
        self.play = wx.Button(self.game_p, label='出牌', pos=(550, 320), size=(120, 70))
        self.play.Bind(wx.EVT_BUTTON, self.OnPlay)
        self.play.SetFont(self.font)
        self.play.Hide()
        self.back = wx.Button(self.game_p, label='返回', pos=(1100, 600), size=(90, 40))
        self.back.Bind(wx.EVT_BUTTON, self.OnBack)
        self.back.SetFont(self.font2)

    def OnGo(self, event):
        self.go.Hide()
        self.back.Hide()
        self.play.Show()
        url = 'http://api.revth.com/game/open'
        headers = {"X-Auth-Token": str(self.token)}
        response = requests.post(url=url, headers=headers)
        dict1 = dict(response.json())
        status = dict1.get('status')
        data = dict1.get('data')
        self.id = data['id']
        self.hand = data['card']
        print('发来的牌' + self.hand)

    def OnPlay(self, event):
        self.play.Hide()
        self.go.Show()
        self.back.Show()
        url = 'http://api.revth.com/game/submit'
        headers = {"X-Auth-Token": str(self.token), "Content-Type": "application/json"}
        final_cards = Biography(str(self.hand))
        form_data = {'id': self.id, 'card': final_cards}
        print(form_data)
        response = requests.post(url=url, headers=headers, data=json.dumps(form_data))
        dict1 = dict(response.json())
        status = dict1.get('status')
        if status == 0:
            msg = '出牌成功'
        elif status == 2002:
            msg = '出千'
        elif status == 2003:
            msg = '不合法墩牌'
        elif status == 2004:
            msg = '战局不存在或已结束'
        elif status == 3001:
            msg = '战局不存在或未结束'
        wx.MessageBox(msg)
        print(status)
        self.id = None
        self.hand = None

    def OnBack(self, event):
        self.Destroy()
        hall = Hall(self.token)
        hall.Show()

    def OnPaintGame(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("gaming.jpg")
        dc.DrawBitmap(bmp, 0, 0)


class Rank(wx.Frame):
    def __init__(self, token):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.token = token
        self.rank_p = None
        self.grid = None
        self.back = None
        self.font = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitRank()

    def InitRank(self):
        url = 'http://api.revth.com/rank'
        response = requests.get(url)
        list1 = response.json()
        list2 = []
        for i in list1:
            x = dict(i)
            list2.append(x)
        lenth = len(list2)
        print(lenth)
        self.rank_p = wx.Panel(self)
        self.rank_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintRank)
        self.grid = wx.grid.Grid(self.rank_p, -1)
        self.grid.CreateGrid(lenth, 3)
        self.grid.SetSize((750, 500))
        self.grid.SetPosition((490, 100))
        for col in range(3):
            self.grid.SetColSize(col, 215)
        for row in range(lenth):
            self.grid.SetRowSize(row, 30)
        self.grid.SetColLabelValue(0, "玩家id")
        self.grid.SetColLabelValue(1, "分数")
        self.grid.SetColLabelValue(2, "玩家昵称")
        self.grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        for i, item in enumerate(list2):
            self.grid.SetCellValue(i, 0, str(list2[i].get('player_id')))
            self.grid.SetCellValue(i, 1, str(list2[i].get('score')))
            self.grid.SetCellValue(i, 2, str(list2[i].get('name')))
            self.grid.SetCellAlignment(i, 0, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            self.grid.SetCellAlignment(i, 1, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            self.grid.SetCellAlignment(i, 2, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        back = wx.Button(self.rank_p, label='返回', pos=(1100, 630), size=(80, 40))
        back.SetFont(self.font)
        back.Bind(wx.EVT_BUTTON, self.OnBack)

    def OnPaintRank(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("hall.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def OnBack(self, event):
        self.Destroy()
        hall = Hall(self.token)
        hall.Show()


class History(wx.Frame):
    def __init__(self, token):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.history_p = None
        self.get_id = None
        self.tip = None
        self.search = None
        self.grid = None
        self.last = None
        self.next = None
        self.page_now = None
        self.searched_id = None
        self.token = token
        self.font = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitHistory()

    def InitHistory(self):
        self.history_p = wx.Panel(self)
        self.history_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintHistory)
        back = wx.Button(self.history_p, label='返回', pos=(1100, 630), size=(80, 40))
        back.SetFont(self.font)
        back.Bind(wx.EVT_BUTTON, self.OnBack)
        self.tip = wx.StaticText(self.history_p, label='请输入玩家id', pos=(450, 100), size=(190, 30))
        self.tip.SetFont(self.font)
        self.get_id = wx.TextCtrl(self.history_p, -1, pos=(645, 100), size=(150, 30))
        self.search = wx.Button(self.history_p, label='搜索', pos=(795, 100), size=(80, 30))
        self.search.SetFont(self.font)
        self.search.Bind(wx.EVT_BUTTON, self.OnSearch)
        self.last = wx.Button(self.history_p, label='上一页', pos=(315, 550), size=(100, 40))
        self.last.SetFont(self.font)
        self.last.Bind(wx.EVT_BUTTON, self.OnLast)
        self.next = wx.Button(self.history_p, label='下一页', pos=(900, 550), size=(100, 40))
        self.next.SetFont(self.font)
        self.next.Bind(wx.EVT_BUTTON, self.OnNext)
        self.grid = wx.grid.Grid(self.history_p, -1)
        self.grid.CreateGrid(10, 4)
        self.grid.SetSize((683, 333))
        self.grid.SetPosition((315, 180))
        self.grid.SetColSize(3, 120)
        self.grid.SetColSize(1, 320)
        for i in range(10):
            self.grid.SetRowSize(i, 30)
        self.grid.SetColLabelValue(0, "对局id")
        self.grid.SetColLabelValue(1, "出牌情况")
        self.grid.SetColLabelValue(2, "分数")
        self.grid.SetColLabelValue(3, "时间戳")

    def OnPaintHistory(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("hall.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def OnBack(self, event):
        self.Destroy()
        hall = Hall(self.token)
        hall.Show()

    def OnSearch(self, event):
        self.page_now = 0
        self.searched_id = self.get_id.GetValue()
        url = 'http://api.revth.com/history'
        headers = {"X-Auth-Token": self.token}
        form_data = {"player_id": int(self.searched_id), "limit": 10, "page": 0}
        response = requests.get(url, headers=headers, params=form_data)
        dict1 = dict(response.json())
        if dict1.get('status') != 0:
            print(dict1)
            wx.MessageBox('错误')
        else:
            list1 = dict1.get('data')
            if list1:
                for i in range(10):
                    if not list1[i]:
                        wx.MessageBox('该玩家战绩未满十条')
                        break
                    self.grid.SetCellValue(i, 0, str(list1[i].get('id')))
                    self.grid.SetCellValue(i, 1, str(list1[i].get('card')))
                    self.grid.SetCellValue(i, 2, str(list1[i].get('score')))
                    self.grid.SetCellValue(i, 3, str(list1[i].get('timestamp')))
            else:
                wx.MessageBox('该玩家未参与过对局')

    def OnLast(self, event):
        self.page_now -= 1
        if self.page_now < 0:
            self.page_now = 0
        else:
            url = 'http://api.revth.com/history'
            headers = {"X-Auth-Token": self.token}
            form_data = {"player_id": int(self.searched_id), "limit": 10, "page": self.page_now}
            response = requests.get(url, headers=headers, params=form_data)
            dict1 = dict(response.json())
            if dict1.get('status') != 0:
                wx.MessageBox('id或token错误！')
            else:
                list1 = dict1.get('data')
                for i, itm in enumerate(list1):
                    self.grid.SetCellValue(i, 0, str(list1[i].get('id')))
                    self.grid.SetCellValue(i, 1, str(list1[i].get('card')))
                    self.grid.SetCellValue(i, 2, str(list1[i].get('score')))
                    self.grid.SetCellValue(i, 3, str(list1[i].get('timestamp')))

    def OnNext(self, event):
        self.page_now += 1
        url = 'http://api.revth.com/history'
        headers = {"X-Auth-Token": self.token}
        form_data = {"player_id": int(self.searched_id), "limit": 10, "page": self.page_now}
        response = requests.get(url, headers=headers, params=form_data)
        dict1 = dict(response.json())
        if dict1.get('status') != 0:
            wx.MessageBox('id或token错误！')
        else:
            list1 = dict1.get('data')
            for i in range(10):
                self.grid.SetCellValue(i, 0, ' ')
                self.grid.SetCellValue(i, 1, ' ')
                self.grid.SetCellValue(i, 2, ' ')
                self.grid.SetCellValue(i, 3, ' ')
            for i, itm in enumerate(list1):
                self.grid.SetCellValue(i, 0, str(list1[i].get('id')))
                self.grid.SetCellValue(i, 1, str(list1[i].get('card')))
                self.grid.SetCellValue(i, 2, str(list1[i].get('score')))
                self.grid.SetCellValue(i, 3, str(list1[i].get('timestamp')))


class FindBattle(wx.Frame):
    def __init__(self, token):
        wx.Frame.__init__(self, None, -1, "福建十三水", size=(1276, 729), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Center()
        self.find_p = None
        self.grid = None
        self.tip = None
        self.get_id = None
        self.search = None
        self.token = token
        self.font = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, faceName='华文行楷')
        self.InitFindBattle()

    def InitFindBattle(self):
        self.find_p = wx.Panel(self)
        self.find_p.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaintFind)
        self.grid = wx.grid.Grid(self.find_p, -1)
        self.grid.CreateGrid(4, 4)
        self.grid.SetSize((683, 193))
        self.grid.SetPosition((400, 200))
        self.grid.SetColSize(3, 120)
        self.grid.SetColSize(1, 320)
        self.grid.SetColLabelValue(0, "玩家id")
        self.grid.SetColLabelValue(1, "出牌情况")
        self.grid.SetColLabelValue(2, "玩家昵称")
        self.grid.SetColLabelValue(3, "分数")
        back = wx.Button(self.find_p, label='返回', pos=(1100, 630), size=(80, 40))
        back.SetFont(self.font)
        back.Bind(wx.EVT_BUTTON, self.OnBack)
        self.tip = wx.StaticText(self.find_p, label='请输入要查询的战局id', pos=(450, 100), size=(190, 30))
        self.tip.SetFont(self.font)
        self.get_id = wx.TextCtrl(self.find_p, -1, pos=(780, 100), size=(150, 30))
        self.search = wx.Button(self.find_p, label='搜索', pos=(935, 100), size=(80, 30))
        self.search.SetFont(self.font)
        self.search.Bind(wx.EVT_BUTTON, self.OnSearch)

    def OnPaintFind(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("hall.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def OnBack(self, event):
        self.Destroy()
        hall = Hall(self.token)
        hall.Show()

    def OnSearch(self, event):
        searched_id = self.get_id.GetValue()
        url = 'http://api.revth.com/history/' + searched_id
        headers = {"X-Auth-Token": self.token}
        response = requests.get(url, headers=headers)
        list1 = dict(response.json()).get('data').get('detail')
        for i in range(4):
            self.grid.SetCellValue(i, 0, str(list1[i].get('player_id')))
            self.grid.SetCellValue(i, 1, str(list1[i].get('card')))
            self.grid.SetCellValue(i, 2, str(list1[i].get('name')))
            self.grid.SetCellValue(i, 3, str(list1[i].get('score')))


if __name__ == '__main__':
    app = wx.App()
    frame = Start()
    frame.Show()
    app.MainLoop()
