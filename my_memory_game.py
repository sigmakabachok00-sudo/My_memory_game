import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QButtonGroup,
    QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox,
    QSpacerItem, QSizePolicy, QMessageBox
)

# ---------------------- Класс Question ----------------------
class Question:
    """Модель вопроса: текст, правильный ответ, список неправильных ответов."""
    def __init__(self, question_text, right_answer, wrong_answers):
        self.question_text = question_text
        self.right_answer = right_answer
        self.wrong_answers = wrong_answers


# ---------------------- Главное окно ----------------------
class MemoryCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Card")
        self.setFixedSize(550, 400)

        # Счётчик текущего вопроса
        self.current_index = 0
        # База вопросов
        self.questions = [
            Question("Столица Франции?", "Париж", ["Марсель", "Лион", "Бордо"]),
            Question("Сколько планет в Солнечной системе?", "8", ["9", "7", "10"]),
            Question("Какой язык самый распространённый в мире?", "Китайский", ["Английский", "Испанский", "Хинди"]),
            Question("Кто написал «Войну и мир»?", "Лев Толстой", ["Достоевский", "Чехов", "Тургенев"]),
            Question("Химический символ кислорода?", "O", ["H", "N", "C"]),
        ]

        # ---------- Виджеты формы вопроса ----------
        self.question_label = QLabel("Вопрос")
        self.question_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.radio_group = QGroupBox("Варианты ответов")
        self.radio_buttons = []          # список QRadioButton
        self.button_group = QButtonGroup(self)
        self.btn_main = QPushButton("Ответить")
        self.btn_main.setFixedSize(150, 30)

        # Создаём 4 переключателя
        radio_layout = QVBoxLayout()
        for i in range(4):
            rb = QRadioButton(f"Вариант {i+1}")
            self.radio_buttons.append(rb)
            self.button_group.addButton(rb)
            radio_layout.addWidget(rb)
        self.radio_group.setLayout(radio_layout)

        # ---------- Виджеты формы ответа ----------
        self.result_label = QLabel("Результат")
        self.result_label.setStyleSheet("font-size: 14px;")
        self.correct_answer_label = QLabel("Правильный ответ:")
        self.correct_answer_label.setStyleSheet("font-size: 14px; color: blue;")

        # Изначально форма ответа скрыта
        self.result_label.hide()
        self.correct_answer_label.hide()

        # ---------- Компоновка ----------
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.question_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.radio_group)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.btn_main, alignment=Qt.AlignCenter)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Добавляем виджеты ответа в тот же layout (они будут скрыты/показаны)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.correct_answer_label, alignment=Qt.AlignCenter)

        # Подключаем кнопку
        self.btn_main.clicked.connect(self.start_test)

        # Загружаем первый вопрос
        self.ask(self.questions[0])

    # ---------------------- Логика переключения форм ----------------------
    def show_question_form(self):
        """Показать форму вопроса, скрыть форму ответа."""
        self.question_label.show()
        self.radio_group.show()
        self.result_label.hide()
        self.correct_answer_label.hide()

    def show_result_form(self):
        """Скрыть форму вопроса, показать форму ответа."""
        self.question_label.hide()
        self.radio_group.hide()
        self.result_label.show()
        self.correct_answer_label.show()

    def reset_radio_buttons(self):
        """Снять выделение со всех переключателей."""
        for rb in self.radio_buttons:
            rb.setChecked(False)

    # ---------------------- Работа с вопросом ----------------------
    def ask(self, question):
        """Заполнить интерфейс данными вопроса и перемешать варианты."""
        self.question_label.setText(question.question_text)

        # Собираем все варианты и перемешиваем
        all_answers = [question.right_answer] + question.wrong_answers
        random.shuffle(all_answers)

        # Заполняем переключатели (если вариантов меньше 4, лишние скрываем)
        for i, rb in enumerate(self.radio_buttons):
            if i < len(all_answers):
                rb.setText(all_answers[i])
                rb.show()
            else:
                rb.hide()

        # Сохраняем правильный ответ для дальнейших проверок
        self.current_right_answer = question.right_answer

        # Сбрасываем выбор
        self.reset_radio_buttons()

        # Показываем форму вопроса
        self.show_question_form()

    def check_answer(self):
        """Проверить выбранный ответ и вернуть строку результата."""
        selected = None
        for rb in self.radio_buttons:
            if rb.isChecked():
                selected = rb.text()
                break

        if selected is None:
            QMessageBox.warning(self, "Внимание", "Выберите вариант ответа!")
            return None   # сигнал, что ответа нет

        if selected == self.current_right_answer:
            return f"Правильно! Ответ: {self.current_right_answer}"
        else:
            return f"Неправильно! Правильный ответ: {self.current_right_answer}"

    def show_correct(self, message):
        """Отобразить сообщение в форме ответа."""
        self.result_label.setText(message)
        if "Правильно" not in message:
            self.correct_answer_label.setText(f"Правильный ответ: {self.current_right_answer}")
        else:
            self.correct_answer_label.setText(f"Верно! Это {self.current_right_answer}")

    # ---------------------- Обработчики нажатий ----------------------
    def start_test(self):
        """Главный обработчик кнопки (посредник)."""
        if self.btn_main.text() == "Ответить":
            self.show_result()
        else:
            self.next_question()
            self.show_question()

    def show_result(self):
        """Действие при нажатии 'Ответить'."""
        result = self.check_answer()
        if result is None:   # ответ не выбран
            return
        self.show_correct(result)
        self.btn_main.setText("Следующий вопрос")
        self.show_result_form()

    def show_question(self):
        """Действие при нажатии 'Следующий вопрос'."""
        self.show_question_form()
        self.btn_main.setText("Ответить")
        self.reset_radio_buttons()

    def next_question(self):
        """Перейти к следующему вопросу в списке (с зацикливанием)."""
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.current_index = 0
        self.ask(self.questions[self.current_index])


# ---------------------- Точка входа ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoryCard()
    window.show()
    sys.exit(app.exec_())