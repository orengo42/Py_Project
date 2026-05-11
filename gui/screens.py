import re
import pygame

try:
    from .button import Button
    from .textbox import TextBox
    from .widgets import Checkbox, OnScreenKeyboard, RadioButton
    from .graph import draw_truth_graph, draw_truth_graph_2d, draw_function_graph
except ImportError:
    from button import Button
    from textbox import TextBox
    from widgets import Checkbox, OnScreenKeyboard, RadioButton
    from graph import draw_truth_graph, draw_truth_graph_2d, draw_function_graph


try:
    from core.checker import check_hypothesis
    from core.values import build_values
    from core.checker2d import (
        check_hypothesis_2d,
        get_counterexample_points,
    )
    from core.function_docs import get_function_docs
except ImportError:
    check_hypothesis = None
    build_values = None
    check_hypothesis_2d = None
    get_counterexample_points = None

    def get_function_docs():
        return []


DEFAULT_START = 1
DEFAULT_END = 10000
MAX_RANGE_VALUE = 10000

BG_DARK = (8, 20, 55)
BG_LIGHT = (20, 14, 48)
CARD = (32, 42, 67)
BORDER = (73, 86, 120)

TEXT = (234, 238, 255)
MUTED = (150, 158, 182)

CYAN = (88, 221, 255)
GREEN = (0, 205, 112)
ORANGE = (255, 190, 90)


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
    "TOO_MANY_POINTS": "Слишком много точек для проверки. Максимум: 10000.",
    "SAME_VARIABLE_NAMES": "Имена переменных x и y не должны совпадать.",
    "EMPTY_VARIABLE_NAME": "Пустое имя переменной.",
    "INVALID_VARIABLE_NAME": "Некорректное имя переменной.",
    "NO_VARIABLES": "Не указаны переменные.",
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

        truth_points.append((point.variable_value, point.value))

    return truth_points


def get_truth_graph_points_2d(result):
    points = []

    for point in result.points:
        points.append(
            (
                point.x_value,
                point.y_value,
                point.value,
                point.error_code,
            )
        )

    return points


def get_numeric_function_points(values_result):
    points = []

    for point in values_result.points:
        if point.error_code is not None:
            continue

        if isinstance(point.value, bool):
            points.append((point.variable_value, 1 if point.value else 0))
            continue

        if isinstance(point.value, (int, float)):
            points.append((point.variable_value, point.value))

    return points


def format_counterexample(value):
    if isinstance(value, tuple):
        return f"({value[0]}, {value[1]})"

    return str(value)


def draw_background(surface, rect):
    for y in range(rect.height):
        t = y / max(1, rect.height - 1)

        r = int(BG_DARK[0] + (BG_LIGHT[0] - BG_DARK[0]) * t)
        g = int(BG_DARK[1] + (BG_LIGHT[1] - BG_DARK[1]) * t)
        b = int(BG_DARK[2] + (BG_LIGHT[2] - BG_DARK[2]) * t)

        pygame.draw.line(
            surface,
            (r, g, b),
            (rect.left, rect.top + y),
            (rect.right, rect.top + y),
        )


def draw_footer(surface, rect, font):
    footer_rect = pygame.Rect(rect.left, rect.bottom - 56, rect.width, 56)
    pygame.draw.rect(surface, (35, 46, 69), footer_rect)

    esc_rect = pygame.Rect(32, footer_rect.top + 16, 38, 24)
    pygame.draw.rect(surface, (58, 70, 95), esc_rect, border_radius=5)

    esc = font.render("Esc", True, MUTED)
    surface.blit(esc, esc.get_rect(center=esc_rect.center))

    text = font.render("вернуться в меню", True, MUTED)
    surface.blit(text, (esc_rect.right + 10, esc_rect.top + 3))


def make_primary_button(rect, text, font, on_click, icon_name="check"):
    return Button(
        rect=rect,
        text=text,
        font=font,
        on_click=on_click,
        bg_color=(0, 205, 112),
        hover_color=(0, 230, 130),
        text_color=(255, 255, 255),
        border_color=(0, 205, 112),
        radius=14,
        icon_name=icon_name,
        icon_color=(255, 255, 255),
    )


class FunctionDocsPanel:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font

        self.visible = False
        self.scroll_offset = 0
        self.content_height = 0

        self.search_box = TextBox(
            rect=(0, 0, 350, 42),
            font=small_font,
            placeholder="Поиск функции...",
            text_color=TEXT,
            placeholder_color=MUTED,
            bg_color=(48, 58, 85),
            border_color=(82, 96, 132),
            active_border_color=CYAN,
        )

        self.docs = get_function_docs()

    def toggle(self):
        self.visible = not self.visible
        self.scroll_offset = 0

        if not self.visible:
            self.search_box.active = False

    def update(self, dt):
        if self.visible:
            self.search_box.update(dt)

    def filter_docs(self):
        query = self.search_box.text.strip().lower()

        if not query:
            return self.docs

        result = []

        for doc in self.docs:
            aliases = " ".join(doc.aliases).lower()

            text = (
                f"{doc.name} "
                f"{doc.signature} "
                f"{doc.category} "
                f"{doc.description} "
                f"{aliases}"
            ).lower()

            if query in text:
                result.append(doc)

        return result

    def handle_event(self, event):
        if not self.visible:
            return False

        panel_rect = pygame.Rect(20, 80, 430, 620)

        if self.search_box.handle_event(event):
            return True

        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()

            if panel_rect.collidepoint(mouse_pos):
                self.scroll_offset -= event.y * 36
                max_scroll = max(0, self.content_height - (panel_rect.height - 110))
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if panel_rect.collidepoint(event.pos):
                return True

        return False

    def draw(self, surface, content_rect):
        if not self.visible:
            return

        panel_rect = pygame.Rect(
            content_rect.left + 20,
            content_rect.top + 80,
            430,
            content_rect.height - 140,
        )

        pygame.draw.rect(surface, (24, 33, 56), panel_rect, border_radius=16)
        pygame.draw.rect(surface, BORDER, panel_rect, 2, border_radius=16)

        title_surface = self.font.render("Все функции", True, CYAN)
        surface.blit(title_surface, (panel_rect.left + 20, panel_rect.top + 16))

        self.search_box.rect.topleft = (panel_rect.left + 20, panel_rect.top + 58)
        self.search_box.draw(surface)

        list_rect = pygame.Rect(
            panel_rect.left + 16,
            self.search_box.rect.bottom + 16,
            panel_rect.width - 32,
            panel_rect.height - 95,
        )

        old_clip = surface.get_clip()
        surface.set_clip(list_rect)

        docs = self.filter_docs()
        y = list_rect.top - self.scroll_offset
        current_category = None

        for doc in docs:
            if doc.category != current_category:
                current_category = doc.category

                category_surface = self.small_font.render(
                    current_category,
                    True,
                    (120, 225, 255),
                )
                surface.blit(category_surface, (list_rect.left + 4, y))
                y += 28

            signature_surface = self.small_font.render(
                doc.signature,
                True,
                TEXT,
            )
            surface.blit(signature_surface, (list_rect.left + 16, y))
            y += 24

            description_surface = self.small_font.render(
                doc.description,
                True,
                MUTED,
            )
            surface.blit(description_surface, (list_rect.left + 16, y))
            y += 24

            if doc.aliases:
                aliases_text = "Псевдонимы: " + ", ".join(doc.aliases)
                aliases_surface = self.small_font.render(
                    aliases_text,
                    True,
                    (135, 145, 170),
                )
                surface.blit(aliases_surface, (list_rect.left + 16, y))
                y += 24

            y += 12

        self.content_height = y - list_rect.top + self.scroll_offset

        surface.set_clip(old_clip)

        max_scroll = max(0, self.content_height - list_rect.height)

        if max_scroll > 0:
            track_rect = pygame.Rect(
                panel_rect.right - 12,
                list_rect.top,
                5,
                list_rect.height,
            )
            pygame.draw.rect(surface, (60, 70, 100), track_rect, border_radius=3)

            thumb_height = max(40, int(list_rect.height * list_rect.height / self.content_height))
            thumb_y = track_rect.top + int(
                (track_rect.height - thumb_height) * self.scroll_offset / max_scroll
            )

            thumb_rect = pygame.Rect(
                track_rect.left,
                thumb_y,
                track_rect.width,
                thumb_height,
            )

            pygame.draw.rect(surface, CYAN, thumb_rect, border_radius=3)


class MenuScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 62, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 22)
        self.button_font = pygame.font.SysFont("arial", 26, bold=True)

        self.check_button = Button(
            rect=(0, 0, 560, 74),
            text="Проверить гипотезу",
            font=self.button_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(24, 116, 255),
            hover_color=(40, 145, 255),
            text_color=(255, 255, 255),
            border_color=(24, 116, 255),
            radius=16,
            icon_name="calculator",
            icon_color=(255, 255, 255),
        )

        self.function_button = Button(
            rect=(0, 0, 560, 74),
            text="Построить функцию",
            font=self.button_font,
            on_click=lambda: self.app.set_screen("function"),
            bg_color=(186, 28, 255),
            hover_color=(213, 42, 255),
            text_color=(255, 255, 255),
            border_color=(186, 28, 255),
            radius=16,
            icon_name="function",
            icon_color=(255, 255, 255),
        )

        self.library_button = Button(
            rect=(0, 0, 560, 74),
            text="Моя библиотека",
            font=self.button_font,
            on_click=self.open_library,
            bg_color=(245, 0, 95),
            hover_color=(255, 32, 120),
            text_color=(255, 255, 255),
            border_color=(245, 0, 95),
            radius=16,
            icon_name="library",
            icon_color=(255, 255, 255),
        )

        self.message = ""

    def open_library(self):
        self.message = "Библиотеку добавим следующим этапом."

    def handle_event(self, event):
        self.check_button.handle_event(event)
        self.function_button.handle_event(event)
        self.library_button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface, content_rect):
        draw_background(surface, content_rect)

        center_x = content_rect.centerx

        title = self.title_font.render("Меню", True, (244, 164, 255))
        title_rect = title.get_rect(center=(center_x, content_rect.top + 92))
        surface.blit(title, title_rect)

        subtitle = self.subtitle_font.render("Выберите режим работы", True, MUTED)
        subtitle_rect = subtitle.get_rect(center=(center_x, content_rect.top + 150))
        surface.blit(subtitle, subtitle_rect)

        self.check_button.rect.center = (center_x, content_rect.top + 245)
        self.function_button.rect.center = (center_x, content_rect.top + 340)
        self.library_button.rect.center = (center_x, content_rect.top + 435)

        self.check_button.draw(surface)
        self.function_button.draw(surface)
        self.library_button.draw(surface)

        if self.message:
            msg = self.subtitle_font.render(self.message, True, MUTED)
            msg_rect = msg.get_rect(center=(center_x, content_rect.bottom - 48))
            surface.blit(msg, msg_rect)


class CheckHypothesisScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.text_font = pygame.font.SysFont("arial", 18, bold=True)
        self.result_font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16, bold=True)
        self.button_font = pygame.font.SysFont("arial", 20, bold=True)

        self.options = [
            Checkbox((0, 0, 24, 24), "Найти контрпримеры", self.text_font),
            Checkbox((0, 0, 24, 24), "График истинности гипотезы", self.text_font),
        ]

        self.variable_mode = "one"

        self.variable_buttons = [
            RadioButton(
                rect=(0, 0, 22, 22),
                text="Одна переменная",
                font=self.text_font,
                group="variables",
                value="one",
                selected_value_getter=lambda: self.variable_mode,
                selected_value_setter=self.set_variable_mode,
            ),
            RadioButton(
                rect=(0, 0, 22, 22),
                text="Две переменные",
                font=self.text_font,
                group="variables",
                value="two",
                selected_value_getter=lambda: self.variable_mode,
                selected_value_setter=self.set_variable_mode,
            ),
        ]

        self.textbox = TextBox(
            rect=(0, 0, 760, 60),
            font=self.button_font,
            placeholder="Например: is_prime(x) or x == 1",
            text_color=TEXT,
            placeholder_color=MUTED,
            bg_color=(48, 58, 85),
            border_color=(82, 96, 132),
            active_border_color=CYAN,
        )

        self.x_start_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text=str(DEFAULT_START),
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.x_end_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text=str(DEFAULT_END),
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.y_start_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text=str(DEFAULT_START),
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.y_end_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text=str(DEFAULT_END),
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.check_button = make_primary_button(
            rect=(0, 0, 260, 58),
            text="Проверить",
            font=self.button_font,
            on_click=self.run_check,
            icon_name="check",
        )

        self.functions_button = Button(
            rect=(0, 0, 170, 42),
            text="Все функции",
            font=self.small_font,
            on_click=self.toggle_functions,
            bg_color=(35, 45, 70),
            hover_color=(50, 65, 100),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
            icon_name="menu",
            icon_color=TEXT,
        )

        self.function_docs_panel = FunctionDocsPanel(self.text_font, self.small_font)

        self.all_counterexamples_button = Button(
            rect=(0, 0, 220, 44),
            text="Контрпримеры",
            font=self.small_font,
            on_click=self.open_counterexamples,
            bg_color=(58, 48, 68),
            hover_color=(75, 62, 90),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
            icon_name="eye",
            icon_color=TEXT,
        )

        self.graph_button = Button(
            rect=(0, 0, 260, 44),
            text="График истинности",
            font=self.small_font,
            on_click=lambda: self.open_graph(1),
            bg_color=(58, 48, 68),
            hover_color=(75, 62, 90),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
            icon_name="graph",
            icon_color=TEXT,
        )

        self.reset_button = Button(
            rect=(0, 0, 250, 50),
            text="Сбросить",
            font=self.button_font,
            on_click=self.reset,
            bg_color=(255, 56, 20),
            hover_color=(255, 82, 46),
            text_color=(255, 255, 255),
            border_color=(255, 56, 20),
            radius=10,
            icon_name="reset",
            icon_color=(255, 255, 255),
        )

        self.save_button = Button(
            rect=(0, 0, 350, 50),
            text="Сохранить в библиотеку",
            font=self.button_font,
            on_click=self.save_to_library,
            bg_color=(20, 135, 255),
            hover_color=(25, 165, 255),
            text_color=(255, 255, 255),
            border_color=(20, 135, 255),
            radius=10,
            icon_name="save",
            icon_color=(255, 255, 255),
        )

        self.keyboard = OnScreenKeyboard(self.small_font, self.textbox)

        self.result_lines = []
        self.last_expression = ""
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []

        self.show_counterexamples_button = False
        self.show_graph_button = False

        self.save_message = ""
        self.graph_dimension = "1d"

        self.scroll_offset = 0
        self.content_height = 0

    def set_variable_mode(self, mode):
        self.variable_mode = mode

    def toggle_functions(self):
        self.function_docs_panel.toggle()

    def get_textboxes(self):
        boxes = [self.textbox, self.x_start_box, self.x_end_box]

        if self.variable_mode == "two":
            boxes.append(self.y_start_box)
            boxes.append(self.y_end_box)

        return boxes

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

    def parse_range_pair(self, start_box, end_box, label):
        if not start_box.text or not end_box.text:
            return None, None, f"Диапазон {label} не должен быть пустым."

        start = int(start_box.text)
        end = int(end_box.text)

        if start < 1 or end < 1:
            return None, None, f"Границы диапазона {label} должны быть положительными."

        if start > end:
            return None, None, f"Левая граница диапазона {label} не может быть больше правой."

        if start > MAX_RANGE_VALUE or end > MAX_RANGE_VALUE:
            return None, None, f"Максимальное значение диапазона {label}: 10000."

        return start, end, None

    def clamp_scroll(self, content_rect):
        max_scroll = max(0, self.content_height - content_rect.height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def run_check(self):
        self.deactivate_all_textboxes()
        self.save_message = ""

        raw_expression = self.textbox.text.strip()
        expression = normalize_expression(raw_expression)

        if not expression:
            self.result_lines = ["Сначала введите гипотезу."]
            return

        x_start, x_end, x_range_error = self.parse_range_pair(
            self.x_start_box,
            self.x_end_box,
            "x",
        )

        if x_range_error is not None:
            self.result_lines = [x_range_error]
            return

        need_counterexamples = self.is_option_selected("Найти контрпримеры")
        need_truth_graph = self.is_option_selected("График истинности гипотезы")

        self.result_lines = []
        self.last_expression = expression
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []
        self.show_counterexamples_button = False
        self.show_graph_button = False
        self.graph_dimension = "1d"

        if self.variable_mode == "one":
            if check_hypothesis is None:
                self.result_lines = ["Не удалось подключить ядро."]
                return

            result = check_hypothesis(
                expression=expression,
                variable_name="x",
                start=x_start,
                end=x_end,
                max_checks=MAX_RANGE_VALUE,
            )

            lines = [f"Гипотеза: {expression}"]

            if result.error_code is not None:
                lines.append(get_error_message(result.error_code))
                self.result_lines = lines
                return

            self.last_counterexamples = result.counterexamples

            if result.is_true:
                lines.append("Результат: гипотеза верна на проверенном диапазоне.")
            else:
                lines.append("Результат: гипотеза неверна на проверенном диапазоне.")

                if result.counterexamples:
                    lines.append(f"Минимальный контрпример: {min(result.counterexamples)}")

            lines.append(f"Проверено значений: {result.checked_count}.")

            if need_counterexamples and self.last_counterexamples:
                self.show_counterexamples_button = True

            if need_truth_graph:
                if build_values is None:
                    lines.append("Модуль графиков из ядра не подключён.")
                else:
                    values_result = build_values(
                        expression=expression,
                        variable_name="x",
                        start=x_start,
                        end=x_end,
                    )

                    if values_result.error_code is not None:
                        lines.append(get_error_message(values_result.error_code))
                        self.result_lines = lines
                        return

                    truth_points = get_truth_graph_points(values_result)

                    if truth_points is None:
                        lines.append("График истинности можно строить только для булевой гипотезы.")
                    else:
                        self.graph_dimension = "1d"
                        self.available_graph_numbers.append(1)
                        self.graph_data[1] = truth_points
                        self.show_graph_button = True

            self.result_lines = lines
            return

        y_start, y_end, y_range_error = self.parse_range_pair(
            self.y_start_box,
            self.y_end_box,
            "y",
        )

        if y_range_error is not None:
            self.result_lines = [y_range_error]
            return

        if check_hypothesis_2d is None or get_counterexample_points is None:
            self.result_lines = ["Не удалось подключить модуль проверки двух переменных."]
            return

        result_2d = check_hypothesis_2d(
            expression=expression,
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end,
            x_variable_name="x",
            y_variable_name="y",
            max_points=MAX_RANGE_VALUE,
        )

        lines = [f"Гипотеза: {expression}"]

        if result_2d.error_code is not None:
            lines.append(get_error_message(result_2d.error_code))
            self.result_lines = lines
            return

        counterexamples = get_counterexample_points(result_2d)
        self.last_counterexamples = counterexamples

        if result_2d.is_true:
            lines.append("Результат: гипотеза верна на проверенном диапазоне.")
        else:
            lines.append("Результат: гипотеза неверна на проверенном диапазоне.")

            if counterexamples:
                first_counterexample = counterexamples[0]
                lines.append(
                    "Первый найденный контрпример: "
                    f"({first_counterexample[0]}, {first_counterexample[1]})"
                )

        lines.append(f"Проверено пар значений: {result_2d.checked_count}.")

        if need_counterexamples and counterexamples:
            self.show_counterexamples_button = True

        if need_truth_graph:
            self.graph_dimension = "2d"
            self.available_graph_numbers.append(2)
            self.graph_data[2] = get_truth_graph_points_2d(result_2d)
            self.show_graph_button = True

        self.result_lines = lines

    def open_counterexamples(self):
        if not self.last_counterexamples:
            return

        self.app.open_counterexamples(
            self.last_expression,
            self.last_counterexamples,
        )

    def open_graph(self, graph_number):
        if self.graph_dimension == "2d":
            graph_number = 2

        if graph_number not in self.available_graph_numbers:
            return

        self.app.open_graph(
            graph_number,
            self.last_expression,
            self.graph_data.get(graph_number, []),
        )

    def save_to_library(self):
        self.save_message = "Сохранение в библиотеку добавим позже."

    def reset(self):
        for option in self.options:
            option.checked = False

        self.variable_mode = "one"

        self.textbox.clear()
        self.x_start_box.set_text(str(DEFAULT_START))
        self.x_end_box.set_text(str(DEFAULT_END))
        self.y_start_box.set_text(str(DEFAULT_START))
        self.y_end_box.set_text(str(DEFAULT_END))

        self.result_lines = []
        self.last_expression = ""
        self.last_counterexamples = []
        self.graph_data = {}
        self.available_graph_numbers = []

        self.show_counterexamples_button = False
        self.show_graph_button = False

        self.save_message = ""
        self.scroll_offset = 0
        self.graph_dimension = "1d"

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
        if self.show_counterexamples_button:
            if self.all_counterexamples_button.handle_event(event):
                return True

        if self.show_graph_button:
            if self.graph_button.handle_event(event):
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

        if self.function_docs_panel.handle_event(event):
            return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 45
            return

        if self.keyboard.handle_event(event):
            return

        if self.handle_result_buttons(event):
            return

        if self.functions_button.handle_event(event):
            return

        if self.check_button.handle_event(event):
            return

        for option in self.options:
            if option.handle_event(event):
                return

        for radio in self.variable_buttons:
            if radio.handle_event(event):
                return

        if self.handle_textbox_mouse_event(event):
            return

        if self.handle_textbox_key_event(event):
            return

    def update(self, dt):
        for textbox in self.get_textboxes():
            textbox.update(dt)

        self.function_docs_panel.update(dt)

    def draw_range_inputs(self, surface, center_x, y, label, start_box, end_box):
        label_surface = self.text_font.render(f"Диапазон проверки {label}:", True, TEXT)
        from_surface = self.small_font.render("от", True, MUTED)
        to_surface = self.small_font.render("до", True, MUTED)
        max_surface = self.small_font.render("(макс. 10000)", True, MUTED)

        total_width = 180 + 28 + 96 + 35 + 96 + 120
        x = center_x - total_width // 2

        surface.blit(label_surface, label_surface.get_rect(midleft=(x, y + 21)))
        surface.blit(from_surface, from_surface.get_rect(midleft=(x + 190, y + 21)))

        start_box.rect.topleft = (x + 220, y)
        start_box.draw(surface)

        surface.blit(
            to_surface,
            to_surface.get_rect(midleft=(start_box.rect.right + 16, y + 21)),
        )

        end_box.rect.topleft = (start_box.rect.right + 45, y)
        end_box.draw(surface)

        surface.blit(
            max_surface,
            max_surface.get_rect(midleft=(end_box.rect.right + 18, y + 21)),
        )

    def draw_result(self, surface, x, y):
        if not self.result_lines:
            return y

        result_height = 250

        if self.show_counterexamples_button or self.show_graph_button:
            result_height += 60

        card_rect = pygame.Rect(x, y, 760, result_height)
        pygame.draw.rect(surface, (50, 36, 54), card_rect, border_radius=14)
        pygame.draw.rect(surface, (140, 42, 58), card_rect, 1, border_radius=14)

        current_y = card_rect.top + 28

        icon_center = (card_rect.left + 42, current_y + 12)
        pygame.draw.circle(surface, (255, 120, 120), icon_center, 14, 2)
        pygame.draw.line(
            surface,
            (255, 120, 120),
            (icon_center[0] - 6, icon_center[1] - 6),
            (icon_center[0] + 6, icon_center[1] + 6),
            3,
        )
        pygame.draw.line(
            surface,
            (255, 120, 120),
            (icon_center[0] + 6, icon_center[1] - 6),
            (icon_center[0] - 6, icon_center[1] + 6),
            3,
        )

        title_surface = self.button_font.render("Результаты проверки", True, (255, 150, 150))
        surface.blit(title_surface, (card_rect.left + 68, current_y))

        current_y += 42

        for line in self.result_lines:
            color = TEXT

            if "неверна" in line:
                color = (255, 150, 150)
            elif "верна" in line:
                color = (100, 255, 170)
            elif "контрпример" in line:
                color = ORANGE

            line_surface = self.result_font.render(line, True, color)
            surface.blit(line_surface, (card_rect.left + 32, current_y))
            current_y += 32

        current_y += 12
        pygame.draw.line(
            surface,
            (90, 70, 95),
            (card_rect.left + 28, current_y),
            (card_rect.right - 28, current_y),
            1,
        )
        current_y += 18

        button_x = card_rect.left + 28

        if self.show_counterexamples_button:
            self.all_counterexamples_button.rect.topleft = (button_x, current_y)
            self.all_counterexamples_button.draw(surface)
            button_x += 235

        if self.show_graph_button:
            self.graph_button.rect.topleft = (button_x, current_y)
            self.graph_button.draw(surface)

        current_y += 64

        self.save_button.rect.topleft = (card_rect.left + 28, current_y)
        self.reset_button.rect.topleft = (self.save_button.rect.right + 16, current_y)

        self.save_button.draw(surface)
        self.reset_button.draw(surface)

        current_y += 64

        if self.save_message:
            msg = self.small_font.render(self.save_message, True, (100, 255, 170))
            surface.blit(msg, (card_rect.left + 32, current_y))
            current_y += 28

        return max(card_rect.bottom, current_y) + 30

    def draw(self, surface, content_rect):
        draw_background(surface, content_rect)
        self.clamp_scroll(content_rect)

        center_x = content_rect.centerx
        base_y = content_rect.top - self.scroll_offset

        self.functions_button.rect.topleft = (28, base_y + 18)
        self.functions_button.draw(surface)

        title = self.title_font.render("Выбрать опции", True, CYAN)
        title_rect = title.get_rect(center=(center_x, base_y + 58))
        surface.blit(title, title_rect)

        options_x = center_x - 410
        options_y = base_y + 120

        self.options[0].rect.topleft = (options_x + 14, options_y + 18)
        self.options[1].rect.topleft = (options_x + 420, options_y + 18)

        for option in self.options:
            option.draw(surface)

        radio_y = options_y + 98
        radio_card_width = 250
        radio_gap = 20
        radio_group_width = radio_card_width * 2 + radio_gap
        radio_start_x = center_x - radio_group_width // 2

        self.variable_buttons[0].rect.topleft = (
            radio_start_x + 14,
            radio_y + 15,
        )
        self.variable_buttons[1].rect.topleft = (
            radio_start_x + radio_card_width + radio_gap + 14,
            radio_y + 15,
        )

        self.variable_buttons[0].draw(surface)
        self.variable_buttons[1].draw(surface)

        range_card_top = base_y + 305
        range_card_height = 90 if self.variable_mode == "one" else 150
        range_card = pygame.Rect(center_x - 410, range_card_top, 820, range_card_height)

        pygame.draw.rect(surface, CARD, range_card, border_radius=14)
        pygame.draw.rect(surface, BORDER, range_card, 1, border_radius=14)

        self.draw_range_inputs(
            surface,
            center_x,
            range_card.top + 24,
            "x",
            self.x_start_box,
            self.x_end_box,
        )

        if self.variable_mode == "two":
            self.draw_range_inputs(
                surface,
                center_x,
                range_card.top + 84,
                "y",
                self.y_start_box,
                self.y_end_box,
            )

        input_y = range_card.bottom + 28

        label = self.text_font.render("Формула гипотезы", True, TEXT)
        surface.blit(label, (center_x - 410, input_y))

        self.textbox.rect.topleft = (center_x - 410, input_y + 34)
        self.textbox.draw(surface)

        current_y = self.textbox.rect.bottom + 18

        if self.textbox.active:
            self.keyboard.rebuild(center_x, current_y)
            self.keyboard.draw(surface)
            current_y += self.keyboard.get_height() + 28

        self.check_button.rect.center = (center_x, current_y + 29)
        self.check_button.draw(surface)

        result_y = self.check_button.rect.bottom + 34
        result_y = self.draw_result(surface, center_x - 410, result_y)

        draw_footer(surface, content_rect, self.small_font)
        self.function_docs_panel.draw(surface, content_rect)

        self.content_height = max(
            result_y - content_rect.top + self.scroll_offset + 70,
            content_rect.height,
        )
        self.clamp_scroll(content_rect)


class FunctionScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.text_font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16, bold=True)
        self.button_font = pygame.font.SysFont("arial", 20, bold=True)

        self.function_box = TextBox(
            rect=(0, 0, 760, 60),
            font=self.button_font,
            placeholder="Например: phi(x), x ** 2, tau(x)",
            text_color=TEXT,
            placeholder_color=MUTED,
            bg_color=(48, 58, 85),
            border_color=(82, 96, 132),
            active_border_color=CYAN,
        )

        self.start_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text="1",
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.end_box = TextBox(
            rect=(0, 0, 96, 42),
            font=self.button_font,
            text="100",
            numbers_only=True,
            max_length=5,
            text_color=TEXT,
            bg_color=(55, 66, 95),
            border_color=(92, 106, 140),
            active_border_color=CYAN,
        )

        self.build_button = make_primary_button(
            rect=(0, 0, 260, 58),
            text="Построить",
            font=self.button_font,
            on_click=self.build_function,
            icon_name="function",
        )

        self.functions_button = Button(
            rect=(0, 0, 170, 42),
            text="Все функции",
            font=self.small_font,
            on_click=self.toggle_functions,
            bg_color=(35, 45, 70),
            hover_color=(50, 65, 100),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
            icon_name="menu",
            icon_color=TEXT,
        )

        self.function_docs_panel = FunctionDocsPanel(self.text_font, self.small_font)

        self.reset_button = Button(
            rect=(0, 0, 250, 50),
            text="Сбросить",
            font=self.button_font,
            on_click=self.reset,
            bg_color=(255, 56, 20),
            hover_color=(255, 82, 46),
            text_color=(255, 255, 255),
            border_color=(255, 56, 20),
            radius=10,
            icon_name="reset",
            icon_color=(255, 255, 255),
        )

        self.save_button = Button(
            rect=(0, 0, 350, 50),
            text="Сохранить в библиотеку",
            font=self.button_font,
            on_click=self.save_to_library,
            bg_color=(20, 135, 255),
            hover_color=(25, 165, 255),
            text_color=(255, 255, 255),
            border_color=(20, 135, 255),
            radius=10,
            icon_name="save",
            icon_color=(255, 255, 255),
        )

        self.keyboard = OnScreenKeyboard(self.small_font, self.function_box)

        self.points = []
        self.message = ""

        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0

        self.dragging_graph = False
        self.last_mouse_pos = None
        self.graph_rect = None

    def toggle_functions(self):
        self.function_docs_panel.toggle()

    def parse_range(self):
        if not self.start_box.text or not self.end_box.text:
            return None, None, "Диапазон не должен быть пустым."

        start = int(self.start_box.text)
        end = int(self.end_box.text)

        if start < 1 or end < 1:
            return None, None, "Границы диапазона должны быть положительными."

        if start > end:
            return None, None, "Левая граница не может быть больше правой."

        if start > MAX_RANGE_VALUE or end > MAX_RANGE_VALUE:
            return None, None, "Максимальное значение: 10000."

        return start, end, None

    def build_function(self):
        expression = normalize_expression(self.function_box.text.strip())

        self.points = []
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.dragging_graph = False
        self.last_mouse_pos = None

        if not expression:
            self.message = "Введите функцию."
            return

        start, end, error = self.parse_range()

        if error is not None:
            self.message = error
            return

        if build_values is None:
            self.message = "Функция ядра для построения ещё не подключена."
            return

        result = build_values(
            expression=expression,
            variable_name="x",
            start=start,
            end=end,
        )

        if result.error_code is not None:
            self.message = get_error_message(result.error_code)
            return

        self.points = get_numeric_function_points(result)
        self.message = f"Построено точек: {len(self.points)}."

    def reset(self):
        self.function_box.clear()
        self.start_box.set_text("1")
        self.end_box.set_text("100")

        self.points = []
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0

        self.dragging_graph = False
        self.last_mouse_pos = None

        self.message = ""

    def save_to_library(self):
        self.message = "Сохранение функции в библиотеку добавим позже."

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.set_screen("menu")
            return

        if self.function_docs_panel.handle_event(event):
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.graph_rect is not None:
                if self.graph_rect.collidepoint(event.pos):
                    self.dragging_graph = True
                    self.last_mouse_pos = event.pos
                    return

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_graph = False
                self.last_mouse_pos = None

        if event.type == pygame.MOUSEMOTION:
            if self.dragging_graph and self.last_mouse_pos is not None:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]

                self.pan_x += dx
                self.pan_y += dy

                self.last_mouse_pos = event.pos
                return

        if event.type == pygame.MOUSEWHEEL:
            if self.points:
                if event.y > 0:
                    self.zoom *= 1.15
                else:
                    self.zoom /= 1.15

                self.zoom = max(0.25, min(self.zoom, 10.0))
                return

        if self.keyboard.handle_event(event):
            return

        if self.functions_button.handle_event(event):
            return

        if self.build_button.handle_event(event):
            return

        if self.save_button.handle_event(event):
            return

        if self.reset_button.handle_event(event):
            return

        for textbox in [self.function_box, self.start_box, self.end_box]:
            if textbox.handle_event(event):
                return

    def update(self, dt):
        self.function_box.update(dt)
        self.start_box.update(dt)
        self.end_box.update(dt)
        self.function_docs_panel.update(dt)

    def draw_range_inputs(self, surface, center_x, y):
        label_surface = self.text_font.render("Диапазон:", True, TEXT)
        from_surface = self.small_font.render("от", True, MUTED)
        to_surface = self.small_font.render("до", True, MUTED)
        max_surface = self.small_font.render("(макс. 10000)", True, MUTED)

        total_width = 110 + 28 + 96 + 35 + 96 + 120
        x = center_x - total_width // 2

        surface.blit(label_surface, label_surface.get_rect(midleft=(x, y + 21)))
        surface.blit(from_surface, from_surface.get_rect(midleft=(x + 120, y + 21)))

        self.start_box.rect.topleft = (x + 150, y)
        self.start_box.draw(surface)

        surface.blit(
            to_surface,
            to_surface.get_rect(midleft=(self.start_box.rect.right + 16, y + 21)),
        )

        self.end_box.rect.topleft = (self.start_box.rect.right + 45, y)
        self.end_box.draw(surface)

        surface.blit(
            max_surface,
            max_surface.get_rect(midleft=(self.end_box.rect.right + 18, y + 21)),
        )

    def draw(self, surface, content_rect):
        draw_background(surface, content_rect)

        center_x = content_rect.centerx

        self.functions_button.rect.topleft = (28, content_rect.top + 18)
        self.functions_button.draw(surface)

        title = self.title_font.render("Введите функцию:", True, CYAN)
        title_rect = title.get_rect(center=(center_x, content_rect.top + 58))
        surface.blit(title, title_rect)

        self.function_box.rect.topleft = (center_x - 410, content_rect.top + 125)
        self.function_box.draw(surface)

        current_y = self.function_box.rect.bottom + 18

        if self.function_box.active:
            self.keyboard.rebuild(center_x, current_y)
            self.keyboard.draw(surface)
            current_y += self.keyboard.get_height() + 24

        self.draw_range_inputs(surface, center_x, current_y)

        self.build_button.rect.center = (center_x, current_y + 95)
        self.build_button.draw(surface)

        message_y = self.build_button.rect.bottom + 18

        if self.message:
            message = self.small_font.render(self.message, True, MUTED)
            surface.blit(message, (center_x - 410, message_y))

        graph_top = message_y + 42

        graph_rect = pygame.Rect(
            center_x - 410,
            graph_top,
            820,
            max(170, content_rect.bottom - graph_top - 150),
        )

        self.graph_rect = graph_rect

        draw_function_graph(
            surface,
            graph_rect,
            self.points,
            self.text_font,
            self.small_font,
            self.zoom,
            pygame.mouse.get_pos(),
            self.pan_x,
            self.pan_y,
        )

        buttons_y = graph_rect.bottom + 18

        self.save_button.rect.topleft = (center_x - 410, buttons_y)
        self.reset_button.rect.topleft = (self.save_button.rect.right + 16, buttons_y)

        self.save_button.draw(surface)
        self.reset_button.draw(surface)

        draw_footer(surface, content_rect, self.small_font)
        self.function_docs_panel.draw(surface, content_rect)


class CounterexamplesScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 17, bold=True)

        self.expression = ""
        self.counterexamples = []
        self.lines = []
        self.scroll_offset = 0

        self.back_button = Button(
            rect=(28, 24, 160, 44),
            text="Назад",
            font=self.small_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(38, 48, 76),
            hover_color=(50, 64, 100),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
        )

    def set_data(self, expression, counterexamples):
        self.expression = expression
        self.counterexamples = counterexamples
        self.scroll_offset = 0
        self.lines = []

        values_per_line = 8

        for index in range(0, len(counterexamples), values_per_line):
            part = counterexamples[index:index + values_per_line]
            self.lines.append(", ".join(format_counterexample(value) for value in part))

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
        draw_background(surface, content_rect)
        center_x = content_rect.centerx

        self.back_button.draw(surface)

        title = self.title_font.render("Контрпримеры", True, CYAN)
        surface.blit(title, title.get_rect(center=(center_x, content_rect.top + 70)))

        expression = self.text_font.render(f"Гипотеза: {self.expression}", True, TEXT)
        surface.blit(expression, expression.get_rect(center=(center_x, content_rect.top + 128)))

        count = self.text_font.render(f"Всего контрпримеров: {len(self.counterexamples)}", True, MUTED)
        surface.blit(count, count.get_rect(center=(center_x, content_rect.top + 165)))

        list_rect = pygame.Rect(
            content_rect.left + 80,
            content_rect.top + 210,
            content_rect.width - 160,
            content_rect.height - 280,
        )

        pygame.draw.rect(surface, CARD, list_rect, border_radius=14)
        pygame.draw.rect(surface, BORDER, list_rect, 2, border_radius=14)

        old_clip = surface.get_clip()
        surface.set_clip(list_rect)

        y = list_rect.top + 20 - self.scroll_offset

        for line in self.lines:
            line_surface = self.small_font.render(line, True, TEXT)
            surface.blit(line_surface, (list_rect.left + 22, y))
            y += 32

        surface.set_clip(old_clip)
        draw_footer(surface, content_rect, self.small_font)


class GraphScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 17, bold=True)

        self.graph_number = 1
        self.expression = ""
        self.points = []

        self.back_button = Button(
            rect=(28, 24, 160, 44),
            text="Назад",
            font=self.small_font,
            on_click=lambda: self.app.set_screen("check"),
            bg_color=(38, 48, 76),
            hover_color=(50, 64, 100),
            text_color=TEXT,
            border_color=BORDER,
            radius=10,
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

    def draw(self, surface, content_rect):
        draw_background(surface, content_rect)
        center_x = content_rect.centerx

        self.back_button.draw(surface)

        if self.graph_number == 2:
            title_text = "График истинности гипотезы от x и y"
        else:
            title_text = "График истинности гипотезы"

        title = self.title_font.render(title_text, True, CYAN)
        surface.blit(title, title.get_rect(center=(center_x, content_rect.top + 70)))

        expression = self.text_font.render(f"Выражение: {self.expression}", True, TEXT)
        surface.blit(expression, expression.get_rect(center=(center_x, content_rect.top + 130)))

        graph_rect = pygame.Rect(
            content_rect.left + 70,
            content_rect.top + 175,
            content_rect.width - 140,
            content_rect.height - 245,
        )

        if self.graph_number == 2:
            draw_truth_graph_2d(
                surface,
                graph_rect,
                self.points,
                self.text_font,
                self.small_font,
                pygame.mouse.get_pos(),
            )
        else:
            draw_truth_graph(
                surface,
                graph_rect,
                self.points,
                self.text_font,
                self.small_font,
                pygame.mouse.get_pos(),
            )

        draw_footer(surface, content_rect, self.small_font)