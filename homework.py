from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {tt};'
                    ' Длительность: {drtn:.3f} ч.;'
                    ' Дистанция: {dstnc:.3f} км;'
                    ' Ср. скорость: {spd:.3f} км/ч;'
                    ' Потрачено ккал: {clrs:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(
            tt=self.training_type,
            drtn=self.duration,
            dstnc=self.distance,
            spd=self.speed,
            clrs=self.calories
        )


@dataclass
class Training:
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar = 0.65
    M_IN_KM: ClassVar = 1000
    MIN_IN_H: ClassVar = 60

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
    height: int
    CALORIES_WEIGHT_MULTIPLIER: ClassVar = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar = 0.029
    KMH_IN_MSEC: ClassVar = round(
        Training.M_IN_KM
        / (
            Training.MIN_IN_H
            * Training.MIN_IN_H
        ), 3
    )
    CM_IN_M: ClassVar = 100

    def __post_init__(self):
        super().__init__(
            self.action,
            self.duration,
            self.weight
        )
        self.height = self.height / self.CM_IN_M
        self.mean_speed_in_m = (
            self.get_mean_speed()
            * self.KMH_IN_MSEC
        )

    def get_spent_calories(self) -> float:
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
    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar = 1.38
    MEAN_SPEED_MULTIPLER: ClassVar = 1.1
    HEIGHT_MULTIPLER: ClassVar = 2

    def __post_init__(self):
        self.length_pool = self.length_pool
        self.count_pool = self.count_pool
        super().__init__(
            self.action,
            self.duration,
            self.weight
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
    if workout_type in PACK_ACTIONS:
        print(len(data))
        print(Running.__repr__())
        return PACK_ACTIONS[workout_type](*data)


def main(training: Training):
    print(
        training
        .show_training_info()
        .get_message()
    )


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
