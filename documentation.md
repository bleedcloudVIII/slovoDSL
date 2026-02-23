## Примеры синтаксиса

### Линки

#### Link - Используется для слоёв
```
Dense(90) -> Dense(10; sigmoid)
```

#### ReverseLink - Используется для присваивания

##### Присваивание слоя переменной
```
c <- Dense(60; sigmoid)
```

##### Считывание данных из файла
``` 
a <- "input_a.txt"
b <- "input_b.txt"
space <- "c.txt"
```

### Слои:

#### Обычный скрытые слои

##### Dense
```
Dense(50; sigmoid; bias)
```

##### Другие примеры:
```
basis_1 <- {10, 20, 30, 4, 5, 6, 7}
start <- Dense(70)
hidden <- Dense(7; sigmoid; basis_1)
end <- Dense(10; cos)

start -> hidden -> end
```


### Свободные члены
```
# Числа
bias_1 <- {10, 20, 30, 50, 60}

Dense(80) -> Dense(20; cos; bias_1) -> Dense(30)
```

### Свёрточные слои

TODO