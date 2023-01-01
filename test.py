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


def show_training_info(self) -> InfoMessage:
    """Вернуть информационное сообщение о выполненной тренировке"""
    return (InfoMessage('test',
            1.25, 150,
            4.0, 3.525))


test = InfoMessage('test',
                   1.25, 150,
                   4.0, 3.525)
# info: InfoMessage = training.show_training_info()
print(test.get_message(show_training_info()))
