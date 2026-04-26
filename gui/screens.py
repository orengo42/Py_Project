import re
import pygame

try:
    from .button import Button
    from .textbox import TextBox
    from .widgets import Checkbox, OnScreenKeyboard
    from .graph import draw_truth_graph
except ImportError:
    from button import Button
    from textbox import TextBox
    from widgets import Checkbox, OnScreenKeyboard
    from graph import draw_truth_graph


try:
    from core.checker import check_hypothesis
    from core.values import build_values, get_graph_points
except ImportError:
    check_hypothesis = None
    build_values = None
    get_graph_points = None


DEFAULT_START = 1
DEFAULT_END = 10000
MAX_RANGE_VALUE = 10000


ERROR_MESSAGES = {
    "INVALID_RANGE": "Некорректный диапазон проверки.",
    "EMPTY_EXPRESSION": "Пустое выражение.",
    "VARIABLE_NAME_CONFLICT": "Имя переменной совпадает с именем функции.",
    "SYNTAX_ERROR": "Синтаксическая ошибка в выражении.",
    "FORBIDDEN_EXPRESSION": "В выражении есть запрещённая конструкция.",
    "UNKNOWN_NAME": "В выражении есть неизвестное имя.",
    "FORBIDDEN_FUNCTION_CALL": "Запрещённый вызов функции.",
    "UNKNOWN_FUNCTION": "Неизвестная функция.",
    "FORBIDDEN_CONSTANT": "Запрещённая константа.",
    "COMPILE_ERROR": "Ошибка компиляции выражения.",
    "DIVISION_BY_ZERO": "Деление на ноль.",
    "OVERFLOW_ERROR": "Слишком большое значение.",
    "TYPE_ERROR": "Ошибка типа данных.",
    "VALUE_ERROR": "Некорректное значение для функции.",
    "RUNTIME_ERROR": "Ошибка во время вычисления.",
    "NOT_BOOLEAN_RESULT": "Гипотеза должна возвращать True или False.",
}


def normalize_expression(expression):
    result = expression.strip()

    result = result.replace("≤", "<=")
    result = result.replace("≥", ">=")
    result = result.replace("≠", "!=")
    result = result.replace("¬", " not ")
    result = result.replace("∧", " and ")
    result = result.replace("∨", " or ")

    result = re.sub(r"(?<![!<>=])=(?!=)", "==", result)

    return result


def get_error_message(error_code):
    if error_code is None:
        return ""

    return ERROR_MESSAGES.get(error_code, f"Ошибка: {error_code}")

def get_truth_graph_points(values_result):
    truth_points = []

    for point in values_result.points:
        if point.error_code is not None:
            continue

        if not isinstance(point.value, bool):
            return None

        truth_points.append(
            (
                point.variable_value,
                point.value,
            )
        )

    return truth_points

class MenuScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("arial", 28)

        self.check_button = Button(
            rect=(0, 0, 420, 64),
            text="Проверить гипотезу",
            font=self.button_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(245, 245, 255),
            hover_color=(225, 230, 250),
        )

        self.library_button = Button(
            rect=(0, 0, 420, 64),
            text="Библиотека моих гипотез",
            font=self.button_font,
            on_click=self.open_library,
            bg_color=(245, 245, 255),
            hover_color=(225, 230, 250),
        )

        self.message = ""

    def open_library(self):
        self.message = "Экран библиотеки добавим следующим этапом."

    def handle_event(self, event):
        self.check_button.handle_event(event)
        self.library_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface, content_rect):
        center_x = content_rect.centerx

        title_surface = self.title_font.render("Меню", True, (30, 30, 45))
        title_rect = title_surface.get_rect(center=(center_x, content_rect.top + 120))
        surface.blit(title_surface, title_rect)

        self.check_button.rect.center = (center_x, content_rect.top + 230)
        self.library_button.rect.center = (center_x, content_rect.top + 315)

        self.check_button.draw(surface)
        self.library_button.draw(surface)

        if self.message:
            message_font = pygame.font.SysFont("arial", 20)
            message_surface = message_font.render(self.message, True, (90, 90, 110))
            message_rect = message_surface.get_rect(center=(center_x, content_rect.top + 410))
            surface.blit(message_surface, message_rect)


class CheckHypothesisScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 25)
        self.result_font = pygame.font.SysFont("arial", 25)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.button_font = pygame.font.SysFont("arial", 28)

        self.options = [
            Checkbox((0, 0, 26, 26), "Быстрая проверка (верно/неверно)", self.text_font),
            Checkbox((0, 0, 26, 26), "Найти контрпримеры", self.text_font),
            Checkbox((0, 0, 26, 26), "График истинности гипотезы", self.text_font),
            Checkbox((0, 0, 26, 26), "Построить график 2", self.text_font),
            Checkbox((0, 0, 26, 26), "Построить график 3", self.text_font),
        ]

        self.textbox = TextBox(
            rect=(0, 0, 650, 58),
            font=self.text_font,
            placeholder="Например: is_prime(n) or n == 1",
        )

        self.range_start_box = TextBox(
            rect=(0, 0, 90, 38),
            font=self.small_font,
            text=str(DEFAULT_START),
            numbers_only=True,
            max_length=5,
        )

        self.range_end_box = TextBox(
            rect=(0, 0, 90, 38),
            font=self.small_font,
            text=str(DEFAULT_END),
            numbers_only=True,
            max_length=5,
        )

        self.check_button = Button(
            rect=(0, 0, 260, 58),
            text="Проверить",
            font=self.button_font,
            on_click=self.run_check,
            bg_color=(220, 235, 255),
            hover_color=(200, 220, 250),
            border_color=(120, 150, 210),
        )

        self.all_counterexamples_button = Button(
            rect=(0, 0, 340, 46),
            text="Смотреть все контрпримеры",
            font=self.small_font,
            on_click=self.open_counterexamples,
            bg_color=(245, 245, 255),
            hover_color=(225, 230, 250),
        )

        self.graph_buttons = [
            Button(
                rect=(0, 0, 280, 46),
                text="Смотреть график истинности",
                font=self.small_font,
                on_click=lambda: self.open_graph(1),
                bg_color=(245, 245, 255),
                hover_color=(225, 230, 250),
            ),
            Button(
                rect=(0, 0, 230, 46),
                text="Смотреть график 2",
                font=self.small_font,
                on_click=lambda: self.open_graph(2),
                bg_color=(245, 245, 255),
                hover_color=(225, 230, 250),
            ),
            Button(
                rect=(0, 0, 230, 46),
                text="Смотреть график 3",
                font=self.small_font,
                on_click=lambda: self.open_graph(3),
                bg_color=(245, 245, 255),
                hover_color=(225, 230, 250),
            ),
        ]

        self.reset_button = Button(
            rect=(0, 0, 150, 46),
            text="Сбросить",
            font=self.small_font,
            on_click=self.reset,
            bg_color=(245, 235, 235),
            hover_color=(235, 215, 215),
        )

        self.save_button = Button(
            rect=(0, 0, 330, 46),
            text="Сохранить в свою библиотеку",
            font=self.small_font,
            on_click=self.save_to_library,
            bg_color=(235, 245, 235),
            hover_color=(215, 235, 215),
        )

        self.keyboard = OnScreenKeyboard(self.small_font, self.textbox)

        self.result_lines = []
        self.last_expression = ""
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []
        self.save_message = ""

        self.scroll_offset = 0
        self.content_height = 0

    def get_textboxes(self):
        return [
            self.textbox,
            self.range_start_box,
            self.range_end_box,
        ]

    def deactivate_all_textboxes(self):
        for textbox in self.get_textboxes():
            textbox.active = False

    def get_selected_options(self):
        selected = []

        for option in self.options:
            if option.checked:
                selected.append(option.text)

        return selected

    def is_option_selected(self, option_text):
        return option_text in self.get_selected_options()

    def parse_range(self):
        if not self.range_start_box.text or not self.range_end_box.text:
            return None, None, "Диапазон проверки не должен быть пустым."

        start = int(self.range_start_box.text)
        end = int(self.range_end_box.text)

        if start < 1 or end < 1:
            return None, None, "Границы диапазона должны быть положительными."

        if start > end:
            return None, None, "Левая граница диапазона не может быть больше правой."

        if start > MAX_RANGE_VALUE or end > MAX_RANGE_VALUE:
            return None, None, "Максимальное значение диапазона: 10000."

        return start, end, None

    def clamp_scroll(self, content_rect):
        max_scroll = max(0, self.content_height - content_rect.height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def run_check(self):
        self.deactivate_all_textboxes()
        self.save_message = ""

        if check_hypothesis is None:
            self.result_lines = [
                "Не удалось подключить ядро.",
                "Проверь, что папка core находится рядом с gui.",
            ]
            return

        raw_expression = self.textbox.text.strip()
        expression = normalize_expression(raw_expression)
        selected_options = self.get_selected_options()

        if not expression:
            self.result_lines = ["Сначала введите гипотезу."]
            return

        if not selected_options:
            self.result_lines = ["Выберите хотя бы одну опцию проверки."]
            return

        start, end, range_error = self.parse_range()

        if range_error is not None:
            self.result_lines = [range_error]
            return

        need_fast_check = self.is_option_selected("Быстрая проверка (верно/неверно)")
        need_counterexamples = self.is_option_selected("Найти контрпримеры")
        need_graph_1 = self.is_option_selected("График истинности гипотезы")
        need_graph_2 = self.is_option_selected("Построить график 2")
        need_graph_3 = self.is_option_selected("Построить график 3")
        need_graph = need_graph_1 or need_graph_2 or need_graph_3

        self.result_lines = []
        self.last_expression = expression
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []

        lines = [
            f"Гипотеза: {expression}",
        ]

        if need_fast_check or need_counterexamples:
            max_counterexamples = end - start + 1

            result = check_hypothesis(
                expression=expression,
                variable_name="n",
                start=start,
                end=end,
                max_counterexamples=max_counterexamples,
            )

            if result.error_code is not None:
                lines.append(get_error_message(result.error_code))
                self.result_lines = lines
                return

            self.last_counterexamples = result.counterexamples

            if result.is_true:
                lines.append("Результат: гипотеза верна на проверенном диапазоне.")
                lines.append(f"Проверено значений: {result.checked_count}.")
            else:
                lines.append("Результат: гипотеза неверна на проверенном диапазоне.")
                lines.append(f"Проверено значений: {result.checked_count}.")

                if result.counterexamples:
                    minimum_counterexample = min(result.counterexamples)
                    lines.append(f"Минимальный контрпример: {minimum_counterexample}")

        if need_graph:
          if build_values is None:
              lines.append("Модуль графиков из ядра не подключён.")
          else:
              values_result = build_values(
                  expression=expression,
                  variable_name="n",
                  start=start,
                  end=end,
              )

              if values_result.error_code is not None:
                  lines.append(get_error_message(values_result.error_code))
                  self.result_lines = lines
                  return

              if need_graph_1:
                  truth_points = get_truth_graph_points(values_result)

                  if truth_points is None:
                      lines.append(
                          "График истинности можно строить только для булевой гипотезы "
                          "(то есть выражение должно возвращать True или False)."
                      )
                  else:
                      self.available_graph_numbers.append(1)
                      self.graph_data[1] = truth_points

              if need_graph_2 or need_graph_3:
                  numeric_points = get_graph_points(values_result)

                  if need_graph_2:
                      self.available_graph_numbers.append(2)
                      self.graph_data[2] = numeric_points

                  if need_graph_3:
                      self.available_graph_numbers.append(3)
                      self.graph_data[3] = numeric_points

        self.result_lines = lines

    def open_counterexamples(self):
        if not self.last_counterexamples:
            return

        self.app.open_counterexamples(
            self.last_expression,
            self.last_counterexamples,
        )

    def open_graph(self, graph_number):
      if graph_number not in self.available_graph_numbers:
          return

      points = self.graph_data.get(graph_number, [])

      self.app.open_graph(
          graph_number,
          self.last_expression,
          points,
      )

    def save_to_library(self):
        self.save_message = "Сохранение в библиотеку добавим позже."

    def reset(self):
        for option in self.options:
            option.checked = False

        self.textbox.clear()
        self.range_start_box.set_text(str(DEFAULT_START))
        self.range_end_box.set_text(str(DEFAULT_END))

        self.result_lines = []
        self.last_expression = ""
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []
        self.save_message = ""
        self.scroll_offset = 0

        self.deactivate_all_textboxes()

    def handle_textbox_mouse_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        for textbox in self.get_textboxes():
            if textbox.rect.collidepoint(event.pos):
                self.deactivate_all_textboxes()
                textbox.handle_event(event)
                return True

        self.deactivate_all_textboxes()
        return False

    def handle_textbox_key_event(self, event):
        if event.type != pygame.KEYDOWN:
            return False

        for textbox in self.get_textboxes():
            if textbox.active:
                return textbox.handle_event(event)

        return False

    def handle_result_buttons(self, event):
        if self.last_counterexamples:
            if self.all_counterexamples_button.handle_event(event):
                return True

        for graph_number in self.available_graph_numbers:
            if self.graph_buttons[graph_number - 1].handle_event(event):
                return True

        if self.result_lines:
            if self.save_button.handle_event(event):
                return True

            if self.reset_button.handle_event(event):
                return True

        return False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.set_screen("menu")
            return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 45
            return

        if self.keyboard.handle_event(event):
            return

        if self.handle_result_buttons(event):
            return

        if self.check_button.handle_event(event):
            return

        for option in self.options:
            if option.handle_event(event):
                return

        if self.handle_textbox_mouse_event(event):
            return

        if self.handle_textbox_key_event(event):
            return

    def update(self, dt):
        for textbox in self.get_textboxes():
            textbox.update(dt)

    def draw_range_inputs(self, surface, content_rect, y):
        center_x = content_rect.centerx

        label_surface = self.small_font.render("Диапазон проверки: от", True, (45, 45, 60))
        to_surface = self.small_font.render("до", True, (45, 45, 60))
        max_surface = self.small_font.render(
            "(максимальное значение: 10000)",
            True,
            (120, 120, 140),
        )

        total_width = (
            label_surface.get_width()
            + 10
            + 90
            + 10
            + to_surface.get_width()
            + 10
            + 90
            + 12
            + max_surface.get_width()
        )

        x = center_x - total_width // 2

        label_rect = label_surface.get_rect(midleft=(x, y + 19))
        surface.blit(label_surface, label_rect)

        self.range_start_box.rect.topleft = (label_rect.right + 10, y)
        self.range_start_box.draw(surface)

        to_rect = to_surface.get_rect(midleft=(self.range_start_box.rect.right + 10, y + 19))
        surface.blit(to_surface, to_rect)

        self.range_end_box.rect.topleft = (to_rect.right + 10, y)
        self.range_end_box.draw(surface)

        max_rect = max_surface.get_rect(midleft=(self.range_end_box.rect.right + 12, y + 19))
        surface.blit(max_surface, max_rect)

    def draw_result_lines(self, surface, x, y, max_width):
        current_y = y
        line_gap = 34

        if not self.result_lines:
            hint_surface = self.result_font.render(
                "Результат проверки появится здесь.",
                True,
                (45, 45, 60),
            )
            surface.blit(hint_surface, (x, current_y))
            return current_y + line_gap

        for line in self.result_lines:
            surface_line = self.result_font.render(line, True, (35, 35, 50))
            surface.blit(surface_line, (x, current_y))
            current_y += line_gap

        current_y += 12

        if self.last_counterexamples:
            self.all_counterexamples_button.rect.topleft = (x, current_y)
            self.all_counterexamples_button.draw(surface)
            current_y += 58

        for graph_number in self.available_graph_numbers:
            button = self.graph_buttons[graph_number - 1]
            button.rect.topleft = (x, current_y)
            button.draw(surface)
            current_y += 58

        if self.result_lines:
            self.save_button.rect.topleft = (x, current_y)
            self.save_button.draw(surface)

            self.reset_button.rect.topleft = (
                self.save_button.rect.right + 16,
                current_y,
            )
            self.reset_button.draw(surface)

            current_y += 58

        if self.save_message:
            save_surface = self.small_font.render(
                self.save_message,
                True,
                (60, 110, 60),
            )
            surface.blit(save_surface, (x, current_y))
            current_y += 32

        return current_y

    def draw_scrollbar(self, surface, content_rect):
        max_scroll = max(0, self.content_height - content_rect.height)

        if max_scroll <= 0:
            return

        track_rect = pygame.Rect(
            content_rect.right - 10,
            content_rect.top + 10,
            5,
            content_rect.height - 20,
        )

        pygame.draw.rect(surface, (215, 215, 225), track_rect, border_radius=3)

        visible_ratio = content_rect.height / self.content_height
        thumb_height = max(40, int(track_rect.height * visible_ratio))

        thumb_y = track_rect.top + int(
            (track_rect.height - thumb_height) * self.scroll_offset / max_scroll
        )

        thumb_rect = pygame.Rect(
            track_rect.left,
            thumb_y,
            track_rect.width,
            thumb_height,
        )

        pygame.draw.rect(surface, (140, 140, 160), thumb_rect, border_radius=3)

    def draw(self, surface, content_rect):
        self.clamp_scroll(content_rect)
        center_x = content_rect.centerx
        base_y = content_rect.top - self.scroll_offset

        title_surface = self.title_font.render("Выбрать опции", True, (30, 30, 45))
        title_rect = title_surface.get_rect(center=(center_x, base_y + 60))
        surface.blit(title_surface, title_rect)

        options_x = center_x - 280
        options_y = base_y + 110
        option_gap = 40

        for index, option in enumerate(self.options):
            option.rect.topleft = (options_x, options_y + index * option_gap)
            option.draw(surface)

        self.draw_range_inputs(surface, content_rect, base_y + 320)

        self.textbox.rect.center = (center_x, base_y + 395)
        self.textbox.draw(surface)

        self.check_button.rect.center = (center_x, base_y + 470)
        self.check_button.draw(surface)

        if self.textbox.active:
            keyboard_y = base_y + 545
            self.keyboard.rebuild(center_x, keyboard_y)
            self.keyboard.draw(surface)
            result_y = keyboard_y + 220
        else:
            result_y = base_y + 550

        result_x = options_x
        result_max_width = content_rect.width - result_x - 60

        end_y = self.draw_result_lines(
            surface,
            result_x,
            result_y,
            result_max_width,
        )

        hint_surface = self.small_font.render(
            "Esc — вернуться в меню",
            True,
            (130, 130, 145),
        )
        hint_rect = hint_surface.get_rect(left=24, bottom=content_rect.bottom - 18)
        surface.blit(hint_surface, hint_rect)

        self.content_height = max(
            end_y + self.scroll_offset + 40,
            content_rect.height,
        )

        self.clamp_scroll(content_rect)
        self.draw_scrollbar(surface, content_rect)


class CounterexamplesScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 38, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.expression = ""
        self.counterexamples = []
        self.lines = []
        self.scroll_offset = 0

        self.back_button = Button(
            rect=(24, 66, 180, 42),
            text="Назад",
            font=self.small_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(245, 245, 255),
            hover_color=(225, 230, 250),
        )

    def set_data(self, expression, counterexamples):
        self.expression = expression
        self.counterexamples = counterexamples
        self.scroll_offset = 0
        self.lines = []

        numbers_per_line = 12

        for index in range(0, len(counterexamples), numbers_per_line):
            part = counterexamples[index:index + numbers_per_line]
            self.lines.append(", ".join(str(value) for value in part))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.set_screen("check")
            return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 30
            self.scroll_offset = max(0, self.scroll_offset)
            return

        self.back_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface, content_rect):
        center_x = content_rect.centerx

        self.back_button.draw(surface)

        title_surface = self.title_font.render("Контрпримеры", True, (30, 30, 45))
        title_rect = title_surface.get_rect(center=(center_x, content_rect.top + 70))
        surface.blit(title_surface, title_rect)

        expression_surface = self.text_font.render(
            f"Гипотеза: {self.expression}",
            True,
            (50, 50, 70),
        )
        expression_rect = expression_surface.get_rect(center=(center_x, content_rect.top + 125))
        surface.blit(expression_surface, expression_rect)

        count_surface = self.text_font.render(
            f"Всего контрпримеров: {len(self.counterexamples)}",
            True,
            (50, 50, 70),
        )
        count_rect = count_surface.get_rect(center=(center_x, content_rect.top + 160))
        surface.blit(count_surface, count_rect)

        list_rect = pygame.Rect(
            content_rect.left + 70,
            content_rect.top + 200,
            content_rect.width - 140,
            content_rect.height - 250,
        )

        pygame.draw.rect(surface, (255, 255, 255), list_rect, border_radius=12)
        pygame.draw.rect(surface, (160, 160, 180), list_rect, 2, border_radius=12)

        old_clip = surface.get_clip()
        surface.set_clip(list_rect)

        y = list_rect.top + 18 - self.scroll_offset

        for line in self.lines:
            line_surface = self.small_font.render(line, True, (40, 40, 60))
            surface.blit(line_surface, (list_rect.left + 18, y))
            y += 30

        surface.set_clip(old_clip)


class GraphScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 38, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.graph_number = 1
        self.expression = ""
        self.points = []

        self.back_button = Button(
            rect=(24, 66, 180, 42),
            text="Назад",
            font=self.small_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(245, 245, 255),
            hover_color=(225, 230, 250),
        )

    def set_data(self, graph_number, expression, points):
        self.graph_number = graph_number
        self.expression = expression
        self.points = points

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.set_screen("check")
            return

        self.back_button.handle_event(event)

    def update(self, dt):
        pass

    def draw_graph(self, surface, rect):
        pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=12)
        pygame.draw.rect(surface, (160, 160, 180), rect, 2, border_radius=12)

        if len(self.points) < 2:
            text_surface = self.text_font.render(
                "Недостаточно точек для построения графика.",
                True,
                (90, 90, 110),
            )
            text_rect = text_surface.get_rect(center=rect.center)
            surface.blit(text_surface, text_rect)
            return

        xs = [point[0] for point in self.points]
        ys = [point[1] for point in self.points]

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        if min_y == max_y:
            min_y -= 1
            max_y += 1

        padding = 40

        graph_rect = pygame.Rect(
            rect.left + padding,
            rect.top + padding,
            rect.width - 2 * padding,
            rect.height - 2 * padding,
        )

        pygame.draw.line(
            surface,
            (80, 80, 100),
            (graph_rect.left, graph_rect.bottom),
            (graph_rect.right, graph_rect.bottom),
            2,
        )

        pygame.draw.line(
            surface,
            (80, 80, 100),
            (graph_rect.left, graph_rect.top),
            (graph_rect.left, graph_rect.bottom),
            2,
        )

        screen_points = []

        for x, y in self.points:
            px = graph_rect.left + (x - min_x) / (max_x - min_x) * graph_rect.width
            py = graph_rect.bottom - (y - min_y) / (max_y - min_y) * graph_rect.height
            screen_points.append((int(px), int(py)))

        if len(screen_points) > 1000:
            step = max(1, len(screen_points) // 1000)
            screen_points = screen_points[::step]

        if len(screen_points) >= 2:
            pygame.draw.lines(surface, (50, 90, 180), False, screen_points, 2)

        info_lines = [
            f"x: от {min_x} до {max_x}",
            f"y: от {min_y} до {max_y}",
            f"точек: {len(self.points)}",
        ]

        for index, line in enumerate(info_lines):
            info_surface = self.small_font.render(line, True, (70, 70, 90))
            surface.blit(info_surface, (rect.left + 20, rect.top + 18 + index * 24))

    def draw(self, surface, content_rect):
        center_x = content_rect.centerx

        self.back_button.draw(surface)

        if self.graph_number == 1:
            title_text = "График истинности гипотезы"
        else:
            title_text = f"График {self.graph_number}"

        title_surface = self.title_font.render(
            title_text,
            True,
            (30, 30, 45),
        )
        title_rect = title_surface.get_rect(center=(center_x, content_rect.top + 70))
        surface.blit(title_surface, title_rect)

        expression_surface = self.text_font.render(
            f"Выражение: {self.expression}",
            True,
            (50, 50, 70),
        )
        expression_rect = expression_surface.get_rect(center=(center_x, content_rect.top + 125))
        surface.blit(expression_surface, expression_rect)

        graph_rect = pygame.Rect(
            content_rect.left + 70,
            content_rect.top + 165,
            content_rect.width - 140,
            content_rect.height - 220,
        )

        if self.graph_number == 1:
            draw_truth_graph(
                surface,
                graph_rect,
                self.points,
                self.text_font,
                self.small_font,
            )
        else:
            self.draw_graph(surface, graph_rect)