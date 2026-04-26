import re
import pygame

try:
    from .button import Button
    from .textbox import TextBox
    from .widgets import Checkbox, OnScreenKeyboard
except ImportError:
    from button import Button
    from textbox import TextBox
    from widgets import Checkbox, OnScreenKeyboard


try:
    from core.checker import check_hypothesis
    from core.values import build_values, get_graph_points
except ImportError:
    check_hypothesis = None
    build_values = None
    get_graph_points = None


CHECK_START = 1
CHECK_END = 1000
GRAPH_START = 1
GRAPH_END = 100


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
        self.small_font = pygame.font.SysFont("arial", 20)
        self.button_font = pygame.font.SysFont("arial", 28)

        self.options = [
            Checkbox((0, 0, 26, 26), "Быстрая проверка (верно/неверно)", self.text_font),
            Checkbox((0, 0, 26, 26), "Найти контрпримеры", self.text_font),
            Checkbox((0, 0, 26, 26), "Построить график 1", self.text_font),
            Checkbox((0, 0, 26, 26), "Построить график 2", self.text_font),
            Checkbox((0, 0, 26, 26), "Построить график 3", self.text_font),
        ]

        self.textbox = TextBox(
            rect=(0, 0, 650, 58),
            font=self.text_font,
            placeholder="Например: is_prime(n) or n == 1",
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

        self.keyboard = OnScreenKeyboard(self.small_font, self.textbox)

        self.message_lines = [
            "Пример гипотезы: is_prime(n) or n == 1",
        ]

    def get_selected_options(self):
        selected = []

        for option in self.options:
            if option.checked:
                selected.append(option.text)

        return selected

    def is_option_selected(self, option_text):
        selected_options = self.get_selected_options()
        return option_text in selected_options

    def run_check(self):
        if check_hypothesis is None:
            self.message_lines = [
                "Не удалось подключить ядро.",
                "Проверь, что папка core находится рядом с gui.",
            ]
            return

        raw_expression = self.textbox.text.strip()
        expression = normalize_expression(raw_expression)
        selected_options = self.get_selected_options()

        if not expression:
            self.message_lines = ["Сначала введите гипотезу."]
            return

        if not selected_options:
            self.message_lines = ["Выберите хотя бы одну опцию проверки."]
            return

        need_fast_check = self.is_option_selected("Быстрая проверка (верно/неверно)")
        need_counterexamples = self.is_option_selected("Найти контрпримеры")
        need_graph_1 = self.is_option_selected("Построить график 1")
        need_graph_2 = self.is_option_selected("Построить график 2")
        need_graph_3 = self.is_option_selected("Построить график 3")
        need_graph = need_graph_1 or need_graph_2 or need_graph_3

        lines = []
        lines.append(f"Выражение: {expression}")

        if need_fast_check or need_counterexamples:
            max_counterexamples = 20 if need_counterexamples else 1

            result = check_hypothesis(
                expression=expression,
                variable_name="n",
                start=CHECK_START,
                end=CHECK_END,
                max_counterexamples=max_counterexamples,
            )

            if result.error_code is not None:
                lines.append(get_error_message(result.error_code))
                self.message_lines = lines
                return

            if result.is_true:
                lines.append(f"Гипотеза верна для n от {result.start} до {result.end}.")
                lines.append(f"Проверено значений: {result.checked_count}.")
            else:
                lines.append(f"Гипотеза неверна на проверенном диапазоне.")
                lines.append(f"Проверено значений: {result.checked_count}.")

                if need_counterexamples:
                    lines.append(f"Контрпримеры: {result.counterexamples}")
                else:
                    lines.append(f"Первый найденный контрпример: {result.counterexamples[0]}")

        if need_graph:
            if build_values is None or get_graph_points is None:
                lines.append("Модуль графиков из ядра не подключён.")
            else:
                values_result = build_values(
                    expression=expression,
                    variable_name="n",
                    start=GRAPH_START,
                    end=GRAPH_END,
                )

                if values_result.error_code is not None:
                    lines.append(get_error_message(values_result.error_code))
                    self.message_lines = lines
                    return

                graph_points = get_graph_points(values_result)

                if need_graph_1:
                    lines.append(f"График 1: подготовлено точек: {len(graph_points)}.")

                if need_graph_2:
                    lines.append(f"График 2: подготовлено точек: {len(graph_points)}.")

                if need_graph_3:
                    lines.append(f"График 3: подготовлено точек: {len(graph_points)}.")

                lines.append("Отрисовку графиков добавим следующим этапом.")

        self.message_lines = lines

        print("Raw expression:", raw_expression)
        print("Normalized expression:", expression)
        print("Selected options:", selected_options)
        print("Result:")
        for line in lines:
            print(line)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.set_screen("menu")
            return

        for option in self.options:
            if option.handle_event(event):
                return

        if self.textbox.handle_event(event):
            return

        if self.keyboard.handle_event(event):
            return

        self.check_button.handle_event(event)

    def update(self, dt):
        self.textbox.update(dt)

    def draw(self, surface, content_rect):
        center_x = content_rect.centerx

        title_surface = self.title_font.render("Выбрать опции", True, (30, 30, 45))
        title_rect = title_surface.get_rect(center=(center_x, content_rect.top + 55))
        surface.blit(title_surface, title_rect)

        options_x = center_x - 280
        options_y = content_rect.top + 105
        option_gap = 42

        for index, option in enumerate(self.options):
            option.rect.topleft = (options_x, options_y + index * option_gap)
            option.draw(surface)

        self.textbox.rect.center = (center_x, content_rect.top + 345)
        self.textbox.draw(surface)

        self.check_button.rect.center = (center_x, content_rect.top + 420)
        self.check_button.draw(surface)

        self.keyboard.rebuild(center_x, content_rect.top + 485)
        self.keyboard.draw(surface)

        result_y = content_rect.bottom - 130

        for index, line in enumerate(self.message_lines[:5]):
            message_surface = self.small_font.render(line, True, (70, 70, 90))
            message_rect = message_surface.get_rect(center=(center_x, result_y + index * 24))
            surface.blit(message_surface, message_rect)

        hint_surface = self.small_font.render("Esc — вернуться в меню", True, (130, 130, 145))
        hint_rect = hint_surface.get_rect(left=24, bottom=content_rect.bottom - 18)
        surface.blit(hint_surface, hint_rect)