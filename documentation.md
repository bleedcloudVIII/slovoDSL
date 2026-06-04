## Примеры синтаксиса

### Линки

#### Link
DEPRECATED

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

##### Dense (полносвязный слой)
```
Dense(input_size; function | bias)
```

##### Примеры

```
Dense(50; bias)
```

```
Dense(70)
```

```
Dense(7; sigmoid; {basis_1, start})
```

```
Dense(10; cos; {hidden})
```


##### Другие примеры:
```
start -> hidden -> end
          ^
          |
basis_1 __/
```

```
basis_1 <- Dense(7; {10, 20, 30, 4, 5, 6, 7})
start <- Dense(70)
hidden <- Dense(7; sigmoid; {basis_1, start})
end <- Dense(10; cos; {hidden})
```


### Свободные члены
```
bias_1 <- Dense(5; {10, 20, 30, 50, 60})
```

#### Conv2d (свёрточный слой)
```
Conv2d(kernel_size; offset; padding; stride)
```

```
Conv2d({3, 3})
```

```
Conv2d({3, 3}; {1, 1}; {1, 1})
```

```
Conv2d({3, 3}; {1, 1}; {1, 1}; {2, 2})
```

#### BatchNorm (батч-нормализация)
```
BatchNorm(eps; momentum; dependencies)
```

```
BatchNorm()
```

```
BatchNorm(1e-5)
```

```
BatchNorm(1e-5; 0.1)
```

#### Dropout(p)
```
Dropout(p, dependencies)
```

```
Dropout()
```

```
Dropout(0.5)
```

```
Dropout(0.0)
```

#### ReLU (функция активации)
```
ReLU(dependencies)
```

```
ReLU({layers_1})
```


### Зависимость слоя от другого

#### Пример уже был выше (см. свободные члены)
#### Сначала создаётся нужный слой или операция, затем передаётся в списке в нужный слоё

##### Пример 1
```
start -> end
          ^
          |
basis   __/
```

```
bias <- Dense(5; {1, 2, 3, 4, 5})

start <- Dense(60)
end <- Dense(5; sigmoid; {bias, start})
```

##### Пример 2
###### Структура 
```
    A--
    |  |
    v  |
    B  |
    |  |
    |  |
    | /
    v
    C
```

###### Реализация

```
A <- Dense(5; softmax)
B <- Dense(10; sigmoid, {A})
C <- Dense(20; cos, {B, A})
```


