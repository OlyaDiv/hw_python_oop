from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # имя класса тренировки
    duration: float     # длительность тренировки в часах
    distance: float     # дистанция в километрах
    speed: float        # средняя скорость движения
    calories: float     # количество израсходованных килокалорий

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # длина одного шага
    M_IN_KM: int = 1000     # константа для перевода значений из м в км
    M_IN_HOURS: int = 60    # время тренировки в минутах

    def __init__(
        self,
        action: int,      # количество совершённых действий
        duration: float,  # длительность тренировки
        weight: float,    # вес спортсмена
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_FOR_RUN_1: int = 18  # коэфф-т 1 для расчета калорий при беге
    COEFF_FOR_RUN_2: int = 20  # коэфф-т 2 для расчета калорий при беге

    def get_spent_calories(self) -> float:
        duration_in_mn = self.duration * self.M_IN_HOURS
        return (
            (
                self.COEFF_FOR_RUN_1
                * self.get_mean_speed()
                - self.COEFF_FOR_RUN_2
            )
            * self.weight
            / self.M_IN_KM
            * duration_in_mn
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_FOR_WALK_1: float = 0.035  # коэфф-т 1 для расчета калорий при ходьбе
    COEFF_FOR_WALK_2: float = 0.029  # коэфф-т 2 для расчета калорий при ходьбе

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float  # рост спортсмена
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_mn = self.duration * self.M_IN_HOURS
        return (
            (
                self.COEFF_FOR_WALK_1
                * self.weight
                + (
                    self.get_mean_speed() ** 2
                    // self.height
                )
                * self.COEFF_FOR_WALK_2
                * self.weight
            )
            * duration_in_mn
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38         # длина одного гребка
    COEFF_FOR_SWIM_1: float = 1.1  # коэфф-т 1 для расчета калорий при плавании
    COEFF_FOR_SWIM_2: int = 2      # коэфф-т 2 для расчета калорий при плавании

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,  # длина бассейна в метрах
        count_pool: int      # сколько раз пользователь переплыл бассейн
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed()
                + self.COEFF_FOR_SWIM_1
            )
            * self.COEFF_FOR_SWIM_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_types:
        return training_types[workout_type](*data)
    else:
        raise ValueError(f'Введен неизвестный тип тренировки: {workout_type}.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
