from dataclasses import dataclass, fields, asdict
from typing import ClassVar

MESSAGE = ('Тип тренировки: {training_type};'
           ' Длительность: {duration:.3f} ч.;'
           ' Дистанция: {distance:.3f} км;'
           ' Ср. скорость: {speed:.3f} км/ч;'
           ' Потрачено ккал: {calories:.3f}.')

MSG_ERR_TYPE_ACT = ('\n\nПередан не верный тип тренировки: {workout_type}')
MSG_ERR_TYPE_ARG = ('\n\nПереданно не верное количество аргументов:'
                    ' {len_arg_false} должно быть {len_arg_true}'
                    '\n\nПереданные аргументы: {arg_return}\n')


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return MESSAGE.format(**asdict(self))


@dataclass
class Training:
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.79

    def __post_init__(self):
        super().__init__(self.action, self.duration, self.weight)

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (
                self.duration
                * self.MIN_IN_H
            )
        )


@dataclass
class SportsWalking(Training):
    height: float
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = round(
        Training.M_IN_KM
        / (
            Training.MIN_IN_H
            * Training.MIN_IN_H
        ), 3
    )
    CM_IN_M = 100

    def __init__(self, action, duration, weight, height):
        self.height = height
        super().__init__(
            action,
            duration,
            weight
        )

    def get_spent_calories(self) -> float:
        self.height = self.height / self.CM_IN_M
        self.mean_speed_in_m = (
            self.get_mean_speed()
            * self.KMH_IN_MSEC
        )
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (
                    self.mean_speed_in_m
                    ** 2
                    / self.height
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * (self.duration * self.MIN_IN_H)
        )


@dataclass
class Swimming(Training):
    length_pool: int
    count_pool: int
    LEN_STEP = 1.38
    MEAN_SPEED_MULTIPLER = 1.1
    HEIGHT_MULTIPLER = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(
            action,
            duration,
            weight
        )

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
                + self.MEAN_SPEED_MULTIPLER
            )
            * self.HEIGHT_MULTIPLER
            * self.weight
            * self.duration
        )


PACK_ACTIONS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: int) -> Training:
    if workout_type not in PACK_ACTIONS:
        raise ValueError(MSG_ERR_TYPE_ACT.format(workout_type=workout_type))
    if len(data) != len(fields(PACK_ACTIONS[workout_type])):
        raise ValueError(
            MSG_ERR_TYPE_ARG.format
            (
                len_arg_true=len(data),
                len_arg_false=len
                (
                    fields(PACK_ACTIONS[workout_type])
                ), arg_return=data
            )
        )
#    print(len(fields(PACK_ACTIONS[workout_type])))
    return PACK_ACTIONS[workout_type](*data)


def main(training: Training) -> None:
    print(
        training.
        show_training_info().
        get_message()
    )


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
