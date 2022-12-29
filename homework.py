class InfoMessage:
    """Информационное сообщение о тренировке"""
    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
              f' Длительность: {self.duration:.3f} ч.;'
              f' Дистанция: {self.distance:.3f} км;'
              f' Ср. скорость: {self.speed:.3f} км/ч;'
              f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки"""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """action, тип int — количество совершённых действий (число шагов при
         ходьбе и беге либо гребков — при плавании);
        duration, тип float — длительность тренировки;
        weight, тип float — вес спортсмена."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """расчёт дистанции, которую пользователь преодолел
         за тренировку в км"""
        """action * LEN_STEP / M_IN_KM"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости движения во время тренировки в км/ч"""
        """преодолённая_дистанция_за_тренировку / время_тренировки"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных за тренировку"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке"""
        return (InfoMessage(self.__class__.__name__,
                self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()))


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    """Тренировка: бег"""
    def __init__(self,
                 action,
                 duration,
                 weight
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))
    """Расчёт количества калорий, израсходованных за тренировку"""
    """Расход калорий для бега рассчитывается по такой формуле"""
    """(18 * средняя_скорость + 1.79) * вес_спортсмена / M_IN_KM
     * время_тренировки_в_минутах"""


class SportsWalking(Training):
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    """Тренировка: спортивная ходьба"""
    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ):
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M
        self.mean_speed_in_m = self.get_mean_speed() * self.KMH_IN_MSEC


    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (self.mean_speed_in_m**2 / self.height)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))

    """Расчёт количества калорий, израсходованных за тренировку"""
    """Расчёт калорий для этого класса должен проводиться по такой формуле"""
    """((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2 /
    рост_в_метрах) * 0.029 * вес) * время_тренировки_в_минутах)"""


class Swimming(Training):
    LEN_STEP: float = 1.38
    MEAN_SPEED_MULTIPLER = 1.1
    HEIGHT_MULTIPLER = 2
    """Тренировка: плавание"""
    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: float
                 ):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости движения во время тренировки"""
        """Формула расчёта средней скорости при плавании"""
        """длина_бассейна * count_pool / M_IN_KM / время_тренировки"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:

        """Расчёт количества калорий, израсходованных за тренировку"""
        """Формула для расчёта израсходованных калорий"""
        """(средняя_скорость + 1.1) * 2 * вес * время_тренировки"""
        return ((self.get_mean_speed() + self.MEAN_SPEED_MULTIPLER)
                * self.HEIGHT_MULTIPLER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    pack_list = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in pack_list:
        return pack_list[workout_type](*data)
    """Прочитать данные полученные от датчиков"""


def main(training: Training) -> None:
    """Главная функция"""
    info: InfoMessage = training.show_training_info()
    print (info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
