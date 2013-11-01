from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, NumericProperty, 
    ObjectProperty, DictProperty, ListProperty)
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import pickle
from kivy.network.urlrequest import UrlRequest
from functools import partial
from toast import toast

class RootWidget(Widget):
    pass

class CalendarWidget(Widget):
    popup = ObjectProperty(None)
    current_day = ObjectProperty(None, allownone=True)
    day_data = DictProperty({})

    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)
        Clock.schedule_once(self._init)

    def _init(self, dt):
        self.populate_calendar()
        self.popup = CalendarPopup(title='Did You Rage?', 
            content=CalendarDayPopupContent(),
            size_hint=(.6, .6),
            on_dismiss=self.dismiss_popup)

    def dismiss_popup(self, instance):
        self.set_rage_status(self.current_day, instance.content.rage_status)
        self.current_day.toggle_button.state = 'normal'
        self.current_day = None
        self.save_data()

    def set_rage_status(self, current_day, rage_status):
        previous_type = current_day.toggle_button.button_type
        current_day.toggle_button.button_type = rage_status
        if previous_type != rage_status:
            if previous_type != 'empty':
                self.decrement_type(previous_type, current_day)
            if rage_status != 'empty':
                self.increment_type(rage_status, current_day)

    def increment_type(self, rtype, day):
        request_success = partial(self.increment_request_success, day)
        request_fail = partial(self.increment_request_fail, day)
        if rtype == 'no_rage':
            req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/increment_number_of_tranq',
                on_success=request_success,
                on_failure=request_fail,
                timeout=5.)
        elif rtype == 'rage':
            req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/increment_number_of_rages',
                on_success=request_success, 
                on_failure=request_fail,
                timeout=5.)

    def increment_request_fail(self, day, req, result):
        day.toggle_button.button_type = 'empty'
        toast('Failed to Upload Data for Day: '+ str(
            day.parent.day_number), True)
        self.save_data()

    def increment_request_success(self, day, req, result):
        pass

    def decrement_type(self, rtype, day):
        request_success = partial(self.decrement_request_success, day)
        request_fail = partial(self.decrement_request_fail, day, rtype)
        if rtype == 'no_rage':
            req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/decrement_number_of_tranq',
                on_success=request_success, 
                on_failure=request_fail,
                timeout=5.)
        elif rtype == 'rage':
            req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/decrement_number_of_rages',
                on_success=request_success, 
                on_failure=request_fail,
                timeout=5.)

    def decrement_request_fail(self, day, rtype, req, result):
        toast('Failed to Upload Data for Day: '+ str(
            day.parent.day_number), True)
        day.toggle_button.button_type = rtype
        self.save_data()

    def decrement_request_success(self, day, req, result):
        pass

    def populate_calendar(self):
        layout = self.calendar_layout
        for x in xrange(5):
            layout.add_widget(EmptyCalendarDay())
        for x in xrange(30):
            calendar_day = CalendarDay(day_number=x+1,
                calendar=self)
            layout.add_widget(calendar_day)
            day_dict = {'calendar_object': calendar_day}
            self.day_data[x+1] = day_dict
        self.load_data()

    def load_data(self):
        day_data = self.day_data
        user_data = open('user_data.dogg_this_is_your_data', 'rb')
        data = pickle.load(user_data)
        user_data.close()
        for day_number in day_data:
            day_object = day_data[day_number][
                'calendar_object']
            day_object.day_type = data[day_number]
            day_object.ids.calendar_content.toggle_button.button_type = data[
                day_number]
        
    def save_data(self):
        save_dict = {}
        day_data = self.day_data
        for day_number in day_data:
            save_dict[day_number] = day_data[day_number][
                'calendar_object'].day_type
        output = open('user_data.dogg_this_is_your_data', 'wb')
        pickle.dump(save_dict, output)
        output.close()

    def open_popup(self, current_day):
        content = self.popup.content
        day_type = current_day.toggle_button.button_type
        if day_type != content.rage_status:
            if day_type == 'empty':
                content.ids.no_rage.state = 'normal'
                content.ids.rage.state = 'normal'
                content.rage_status = 'empty'
            elif day_type == 'no_rage':
                content.ids.rage.state = 'normal'
                content.ids.no_rage.state = 'down'
                content.rage_status = 'no_rage'
            elif day_type == 'rage':
                content.ids.rage.state = 'down'
                content.ids.no_rage.state = 'normal'
                content.rage_status = 'rage'
        self.popup.open()
        self.current_day = current_day

class CalendarLabel(Widget):
    text = StringProperty('Default')

class EmptyCalendarDay(Widget):
    pass

class CalendarContent(Widget):
    pass

class CalendarToggleButton(ToggleButton):
    button_type = StringProperty('empty')

class CalendarDay(Widget):
    day_number = NumericProperty(0)
    calendar = ObjectProperty(None)

class CalendarDayPopupContent(Widget):
    rage_status = StringProperty('empty')

class CalendarButton(Button):
    background_color_normal = ListProperty([1., 1., 1., 1.])
    background_color_down = ListProperty([1., 1., 1., 1.])

class CalendarPopup(Popup):
    pass

class NRNApp(App):
    days_of_rage = NumericProperty(0)
    days_of_tranq = NumericProperty(0)

    def build(self):
        self.get_online_data()
    
    def get_online_data(self):
        toast('Getting Latest Data from Server')
        rage_req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/get_number_of_rages',
            on_success=self.rage_request_success, 
            on_failure=self.rage_request_fail,
            timeout=5.)
        no_rage_req = UrlRequest(
            'http://heroku_app_address.herokuapp.com/get_number_of_tranq',
            on_success=self.no_rage_request_success, 
            on_failure=self.no_rage_request_fail,
            timeout=5.)

    def rage_request_fail(self, req, result):
        self.days_of_rage = -1
        toast('Failed to Access Server', True)

    def rage_request_success(self, req, result):
        self.days_of_rage = int(result)

    def no_rage_request_fail(self, req, result):
        self.days_of_tranq = -1
        toast('Failed to Access Server', True)

    def no_rage_request_success(self, req, result):
        self.days_of_tranq = int(result)


if __name__ == '__main__':
    NRNApp().run()
