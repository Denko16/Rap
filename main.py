# main.py — мега-флекс приложение с карточками (готов к сборке в APK)

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
import random
import os
import json
import uuid


# --------------------------Виджеты для даунов
class GlassCard(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 0.08)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            Color(1, 1, 1, 0.2)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)], width=dp(1.5))
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size


class GlowLabel(FloatLayout):
    def __init__(self, text, font_size=dp(36), glow_color=(0.8, 0.4, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.glow = Label(text=text, font_size=font_size + dp(4), bold=True,
                          color=(*glow_color[:3], 0.25), halign='center', valign='center')
        self.main = Label(text=text, font_size=font_size, bold=True,
                          color=glow_color, halign='center', valign='center')
        self.add_widget(self.glow)
        self.add_widget(self.main)
        self.main.texture_update()
        self.glow.texture_update()
        self.size = (max(self.main.texture_size[0], self.glow.texture_size[0]),
                     max(self.main.texture_size[1], self.glow.texture_size[1]))


class GlassButton(ButtonBehavior, FloatLayout):
    def __init__(self, text="", size_hint=(None, None), size=(dp(120), dp(35)), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = size_hint
        self.size = size
        with self.canvas.before:
            Color(1, 1, 1, 0.15)
            self.btn_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            Color(1, 1, 1, 0.35)
            self.btn_border = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)], width=dp(1.5))
        self.bind(pos=self._update, size=self._update)
        self.label = Label(
            text=text, font_size=dp(14), color=(0.9, 0.9, 1, 1), bold=True,
            halign='center', valign='center'
        )
        self.add_widget(self.label)
        self.bind(size=self._update_label_size, pos=self._update_label_pos)

    def _update(self, *args):
        self.btn_bg.pos = self.pos
        self.btn_bg.size = self.size
        self.btn_border.pos = self.pos
        self.btn_border.size = self.size

    def _update_label_size(self, *args):
        self.label.size = self.size
        self.label.text_size = self.size

    def _update_label_pos(self, *args):
        self.label.pos = self.pos

    def on_press(self):
        Animation(opacity=0.7, d=0.1).start(self)
    def on_release(self):
        Animation(opacity=1, d=0.2).start(self)


class FloatingParticle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (dp(random.randint(4, 12)), dp(random.randint(4, 12)))
        self.opacity = random.uniform(0.3, 0.8)
        with self.canvas:
            Color(1, 1, 1, self.opacity)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

    def float_away(self, *args):
        start_y = random.randint(0, 800) 
        self.pos = (random.randint(0, 360), start_y)
        end_y = random.randint(start_y + 200, 1000)
        anim = Animation(y=end_y, opacity=0, d=random.uniform(3, 6))
        anim.bind(on_complete=lambda *x: self.float_away())
        anim.start(self)


# ---------------------------Это сделал Csilit
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.05, 0.02, 0.1, 1)
            Rectangle(pos=(0, 0), size=(1000, 2000))  
            Color(0.6, 0.2, 1, 0.12)
            Ellipse(pos=(-100, 600), size=(400, 400))
            Color(0.1, 0.4, 1, 0.1)
            Ellipse(pos=(200, -150), size=(400, 400))
            Color(1, 0.5, 1, 0.08)
            Ellipse(pos=(50, 50), size=(250, 250))
        for _ in range(12):
            p = FloatingParticle()
            p.float_away()
            layout.add_widget(p)
        card = GlassCard(size_hint=(None, None), size=(dp(300), dp(230)),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title = GlowLabel(text="МЕГА ФЛЕКС", font_size=dp(22),
                          glow_color=(0.8, 0.5, 1, 1), pos_hint={'center_x': 0.5, 'y': 0.65})
        subtitle = GlowLabel(text="Сделал Csilit", font_size=dp(26),
                             glow_color=(0.6, 0.8, 1, 1), pos_hint={'center_x': 0.5, 'y': 0.4})
        btn = GlassButton(text="Круто!", size=(dp(120), dp(35)), pos_hint={'center_x': 0.5, 'y': 0.1})
        btn.bind(on_release=self._go_flex)
        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(btn)
        layout.add_widget(card)
        footer = Label(text="by Csilit", font_size=dp(12), color=(0.5, 0.5, 0.7, 0.8),
                       pos_hint={'center_x': 0.5, 'y': 0.02})
        layout.add_widget(footer)
        self.add_widget(layout)

    def _go_flex(self, instance):
        App.get_running_app().show_flex_overlay()


# ----------------------------Так называемый оверлей
class FlexOverlay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        with self.canvas.before:
            Color(0, 0, 0, 0.85)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.glow = GlowLabel(text="ЭТО СДЕЛАЛ\nCSILIT", font_size=dp(34),
                              glow_color=(1, 0.3, 0.9, 1),
                              pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.glow)
        for _ in range(20):
            p = FloatingParticle()
            p.float_away()
            self.add_widget(p)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def play_and_switch(self, screen_manager):
        anim = Animation(opacity=0, duration=0.8, t='out_quad')
        anim.bind(on_complete=lambda *x: self._after_animation(screen_manager))
        anim.start(self)

    def _after_animation(self, sm):
        if self.parent:
            self.parent.remove_widget(self)
        sm.current = 'menu'


# --------------------------------Менюшка
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks = []
        self.current_sound = None
        self.current_card_id = None

        root = FloatLayout()
        with root.canvas.before:
            Color(0.05, 0.02, 0.1, 1)
            Rectangle(pos=(0, 0), size=(1000, 2000))
            Color(0.5, 0.1, 0.9, 0.1)
            Ellipse(pos=(20, 540), size=(300, 300))
            Color(0.1, 0.6, 1, 0.08)
            Ellipse(pos=(110, -80), size=(350, 350))
        for _ in range(8):
            p = FloatingParticle()
            p.float_away()
            root.add_widget(p)

        title = GlowLabel(text="ТВОЙ РЭП", font_size=dp(24), glow_color=(0.7, 0.5, 1, 1),
                          pos_hint={'center_x': 0.5, 'top': 1})
        root.add_widget(title)

        self.card_title_input = TextInput(
            text="Новая карточка",
            font_size=dp(14),
            background_color=(1, 1, 1, 0.1),
            foreground_color=(1, 1, 1, 0.9),
            cursor_color=(0.8, 0.5, 1, 1),
            padding=[dp(8), dp(8)],
            size_hint=(0.9, None),
            height=dp(36),
            pos_hint={'center_x': 0.5, 'top': 0.93}
        )
        root.add_widget(self.card_title_input)

        text_card = GlassCard(size_hint=(0.9, None), height=dp(180),
                              pos_hint={'center_x': 0.5, 'top': 0.8})
        text_label = Label(text="Текст песни:", font_size=dp(14),
                           color=(0.9, 0.9, 1, 0.8), bold=True,
                           size_hint=(1, None), height=dp(25),
                           pos_hint={'x': 0, 'top': 1})
        text_card.add_widget(text_label)
        self.lyrics_input = TextInput(
            hint_text="Пиши свой реп здесь...",
            font_size=dp(13),
            background_color=(1, 1, 1, 0.1),
            foreground_color=(1, 1, 1, 0.9),
            cursor_color=(0.8, 0.5, 1, 1),
            padding=[dp(8), dp(8)],
            size_hint=(1, None), height=dp(140),
            pos_hint={'x': 0, 'top': 0.8}
        )
        text_card.add_widget(self.lyrics_input)
        root.add_widget(text_card)

        music_card = GlassCard(size_hint=(0.9, None), height=dp(180),
                               pos_hint={'center_x': 0.5, 'y': 0.05})
        music_label = Label(text="Твои биты:", font_size=dp(14),
                            color=(0.9, 0.9, 1, 0.8), bold=True,
                            size_hint=(1, None), height=dp(25),
                            pos_hint={'x': 0, 'top': 1})
        music_card.add_widget(music_label)
        scroll = ScrollView(size_hint=(1, None), height=dp(90),
                            pos_hint={'x': 0, 'top': 0.75})
        self.track_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.track_list.bind(minimum_height=self.track_list.setter('height'))
        scroll.add_widget(self.track_list)
        music_card.add_widget(scroll)

        btn_layout = BoxLayout(size_hint=(1, None), height=dp(35),
                               pos_hint={'x': 0, 'y': 0.05}, spacing=dp(8))
        add_btn = GlassButton(text="Добавить бит", size=(dp(120), dp(30)))
        add_btn.bind(on_release=self._open_filechooser)
        play_btn = GlassButton(text="Играть", size=(dp(80), dp(30)))
        play_btn.bind(on_release=self._play_track)
        stop_btn = GlassButton(text="Стоп", size=(dp(80), dp(30)))
        stop_btn.bind(on_release=self._stop_music)
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(play_btn)
        btn_layout.add_widget(stop_btn)
        music_card.add_widget(btn_layout)
        root.add_widget(music_card)

        card_btn_layout = BoxLayout(size_hint=(0.9, None), height=dp(35),
                                    pos_hint={'center_x': 0.5, 'y': 0.28}, spacing=dp(8))
        save_btn = GlassButton(text="Сохранить", size=(dp(100), dp(30)))
        save_btn.bind(on_release=self._save_current_card)
        save_as_btn = GlassButton(text="Сохранить как", size=(dp(100), dp(30)))
        save_as_btn.bind(on_release=lambda x: self._save_current_card(as_new=True))
        my_cards_btn = GlassButton(text="Мои карточки", size=(dp(120), dp(30)))
        my_cards_btn.bind(on_release=self._go_to_cards)
        card_btn_layout.add_widget(save_btn)
        card_btn_layout.add_widget(save_as_btn)
        card_btn_layout.add_widget(my_cards_btn)
        root.add_widget(card_btn_layout)

        back_btn = GlassButton(text="Назад", size=(dp(70), dp(30)),
                               pos_hint={'x': 0.02, 'top': 0.98})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        root.add_widget(back_btn)

        self.add_widget(root)

    # ---------------------------------Треки и залупа
    def _open_filechooser(self, instance):
        content = BoxLayout(orientation='vertical')
        fc = FileChooserListView(path=os.path.expanduser("~"), filters=['*.mp3', '*.wav', '*.ogg'])
        content.add_widget(fc)
        btns = BoxLayout(size_hint_y=None, height=dp(35))
        cancel = GlassButton(text="Отмена", size=(dp(80), dp(30)))
        select = GlassButton(text="Выбрать", size=(dp(80), dp(30)))
        btns.add_widget(cancel)
        btns.add_widget(select)
        content.add_widget(btns)
        popup = Popup(title="Выбери бит", content=content, size_hint=(0.9, 0.8))
        cancel.bind(on_release=popup.dismiss)
        select.bind(on_release=lambda x: self._add_track(fc.selection, popup))
        popup.open()

    def _add_track(self, selection, popup):
        if selection:
            path = selection[0]
            name = os.path.basename(path)
            self.tracks.append({'path': path, 'name': name, 'sound': None})
            self._update_track_list()
        popup.dismiss()

    def _update_track_list(self):
        self.track_list.clear_widgets()
        for t in self.tracks:
            lbl = Label(text=t['name'], size_hint_y=None, height=dp(30),
                        color=(0.9, 0.9, 1, 0.8), font_size=dp(12),
                        halign='left', valign='middle')
            lbl.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
            self.track_list.add_widget(lbl)

    def _play_track(self, instance):
        if not self.tracks:
            return
        track = self.tracks[-1]
        if track['sound'] is None:
            try:
                track['sound'] = SoundLoader.load(track['path'])
            except Exception as e:
                print("Ошибка загрузки:", e)
                return
        if self.current_sound:
            self.current_sound.stop()
        self.current_sound = track['sound']
        if self.current_sound:
            self.current_sound.play()

    def _stop_music(self, instance):
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None

    # -----------------------------карточки и залупа
    def _save_current_card(self, as_new=False):
        app = App.get_running_app()
        title = self.card_title_input.text.strip()
        if not title:
            title = "Без названия"
        lyrics = self.lyrics_input.text
        track_paths = [t['path'] for t in self.tracks]

        card_data = {
            "title": title,
            "lyrics": lyrics,
            "track_paths": track_paths
        }

        if as_new or self.current_card_id is None:
            new_id = str(uuid.uuid4())
            card_data["id"] = new_id
            app.save_card(card_data)
            self.current_card_id = new_id
        else:
            card_data["id"] = self.current_card_id
            app.save_card(card_data)

        popup = Popup(title="Сохранено", content=Label(text="Карточка сохранена!"),
                      size_hint=(0.6, 0.3))
        popup.open()

    def load_card(self, card_data):
        self.current_card_id = card_data["id"]
        self.card_title_input.text = card_data.get("title", "Без названия")
        self.lyrics_input.text = card_data.get("lyrics", "")
        self.tracks.clear()
        for path in card_data.get("track_paths", []):
            if os.path.exists(path):
                name = os.path.basename(path)
                self.tracks.append({'path': path, 'name': name, 'sound': None})
            else:
                print(f"Файл не найден: {path}")
        self._update_track_list()
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None

    def _go_to_cards(self, instance):
        self.manager.current = 'cards'


# -----------------------Лента карточек
class CardsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0.05, 0.02, 0.1, 1)
            Rectangle(pos=(0, 0), size=(1000, 2000))
            Color(0.6, 0.2, 1, 0.1)
            Ellipse(pos=(-100, 550), size=(350, 350))
            Color(0.1, 0.5, 1, 0.08)
            Ellipse(pos=(160, -100), size=(300, 300))
        title = GlowLabel(text="МОИ КАРТОЧКИ", font_size=dp(24), glow_color=(0.7, 0.5, 1, 1),
                          pos_hint={'center_x': 0.5, 'top': 1})
        self.layout.add_widget(title)
        back_btn = GlassButton(text="Назад", size=(dp(70), dp(30)),
                               pos_hint={'x': 0.02, 'top': 0.98})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(back_btn)
        new_btn = GlassButton(text="Новая карточка", size=(dp(130), dp(30)),
                              pos_hint={'right': 0.98, 'top': 0.98})
        new_btn.bind(on_release=self._new_card)
        self.layout.add_widget(new_btn)

        scroll = ScrollView(pos_hint={'center_x': 0.5, 'top': 0.88}, size_hint=(0.95, 0.8))
        self.cards_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.cards_container.bind(minimum_height=self.cards_container.setter('height'))
        scroll.add_widget(self.cards_container)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def on_enter(self):
        self.refresh_cards()

    def refresh_cards(self):
        self.cards_container.clear_widgets()
        app = App.get_running_app()
        cards = app.get_all_cards()
        if not cards:
            empty_label = Label(text="Нет сохранённых карточек.\nНажмите '+' чтобы создать",
                                font_size=dp(14), color=(0.7, 0.7, 1, 0.8), halign='center')
            self.cards_container.add_widget(empty_label)
            return
        for card in cards:
            card_widget = self._create_card_widget(card)
            self.cards_container.add_widget(card_widget)

    def _create_card_widget(self, card):
        card_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(90), spacing=dp(5))
        card_bg = GlassCard(size_hint=(1, 1))
        inner_layout = BoxLayout(orientation='vertical', padding=dp(8))
        title_label = Label(text=card.get('title', 'Без названия'), font_size=dp(16),
                            color=(1, 1, 1, 0.9), bold=True, size_hint_y=None, height=dp(25),
                            halign='left', valign='middle')
        title_label.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        preview = card.get('lyrics', '')[:60] + ('...' if len(card.get('lyrics', '')) > 60 else '')
        lyrics_preview = Label(text=preview if preview else "(нет текста)", font_size=dp(11),
                               color=(0.8, 0.8, 1, 0.7), size_hint_y=None, height=dp(30),
                               halign='left', valign='top')
        lyrics_preview.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        inner_layout.add_widget(title_label)
        inner_layout.add_widget(lyrics_preview)

        btn_row = BoxLayout(size_hint_y=None, height=dp(25), spacing=dp(8))
        open_btn = GlassButton(text="Открыть", size=(dp(80), dp(25)))
        open_btn.bind(on_release=lambda x, c=card: self._open_card(c))
        delete_btn = GlassButton(text="Удалить", size=(dp(80), dp(25)))
        delete_btn.bind(on_release=lambda x, c=card: self._delete_card(c))
        btn_row.add_widget(open_btn)
        btn_row.add_widget(delete_btn)
        inner_layout.add_widget(btn_row)

        card_bg.add_widget(inner_layout)
        card_box.add_widget(card_bg)
        return card_box

    def _open_card(self, card):
        menu_screen = self.manager.get_screen('menu')
        menu_screen.load_card(card)
        self.manager.current = 'menu'

    def _delete_card(self, card):
        def do_delete(btn):
            app = App.get_running_app()
            app.delete_card(card['id'])
            popup.dismiss()
            self.refresh_cards()
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(text=f'Удалить "{card.get("title")}"?', font_size=dp(14)))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(8))
        yes_btn = GlassButton(text="Да", size=(dp(70), dp(25)))
        yes_btn.bind(on_release=do_delete)
        no_btn = GlassButton(text="Нет", size=(dp(70), dp(25)))
        no_btn.bind(on_release=lambda x: popup.dismiss())
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        popup = Popup(title="Подтверждение", content=content, size_hint=(0.7, 0.35))
        popup.open()

    def _new_card(self, instance):
        app = App.get_running_app()
        new_id = str(uuid.uuid4())
        new_card = {
            "id": new_id,
            "title": "Новая карточка",
            "lyrics": "",
            "track_paths": []
        }
        app.save_card(new_card)
        menu_screen = self.manager.get_screen('menu')
        menu_screen.load_card(new_card)
        self.manager.current = 'menu'


# -----------------------------Приложуха
class FlexApp(App):
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(CardsScreen(name='cards'))
        self.load_cards_store()
        return self.sm

    def show_flex_overlay(self):
        overlay = FlexOverlay()
        self.root.current_screen.add_widget(overlay)
        overlay.play_and_switch(self.root)

    # --------------------------Карточки
    def get_cards_file_path(self):
        # Член в внутреннем хранилеще твоей мамы(в жопе)
        if hasattr(self, 'user_data_dir'):
            return os.path.join(self.user_data_dir, "cards.json")
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards.json")

    def load_cards_store(self):
        path = self.get_cards_file_path()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cards_list = data.get('cards', [])
            except:
                self.cards_list = []
        else:
            self.cards_list = []

    def save_cards_store(self):
        path = self.get_cards_file_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'cards': self.cards_list}, f, ensure_ascii=False, indent=2)
        except:
            pass  #игнор твоей   мамы

    def get_all_cards(self):
        return self.cards_list

    def get_card(self, card_id):
        for card in self.cards_list:
            if card['id'] == card_id:
                return card
        return None

    def save_card(self, card_data):
        card_id = card_data['id']
        existing = self.get_card(card_id)
        if existing:
            existing.update(card_data)
        else:
            self.cards_list.append(card_data)
        self.save_cards_store()

    def delete_card(self, card_id):
        self.cards_list = [c for c in self.cards_list if c['id'] != card_id]
        self.save_cards_store()


if __name__ == '__main__':
    FlexApp().run()