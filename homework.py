from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60
    COEFF_CALORIE_RUN_1: int = 18
    COEFF_CALORIE_RUN_2: int = 20
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('To be implemented')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration_h,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_kcal: float = ((self.COEFF_CALORIE_RUN_1
                                * self.get_mean_speed()
                                - self.COEFF_CALORIE_RUN_2) * self.weight_kg
                                / self.M_IN_KM * self.duration_h
                                * self.HOUR_IN_MIN)
        return calories_kcal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_kcal: float = ((self.COEFF_CALORIE_WLK_1 * self.weight_kg
                                + (self.get_mean_speed() ** 2
                                 // self.height_cm) * self.COEFF_CALORIE_WLK_2
                                * self.weight_kg) * self.duration_h
                                * self.HOUR_IN_MIN)
        return calories_kcal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_kmh: float = (self.length_pool_m * self.count_pool
                            / self.M_IN_KM / self.duration_h)
        return speed_kmh

    def get_spent_calories(self) -> float:
        calories_kcal: float = ((self.get_mean_speed()
                                + self.COEFF_CALORIE_SWM_1)
                                * self.COEFF_CALORIE_SWM_2 * self.weight_kg)
        return calories_kcal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    if workout_type in dictionary:
        return dictionary[workout_type](*data)
    else:
        print(f'{workout_type} is undefined')
        return exit()


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
