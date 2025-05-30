# Модуль dcache

Модуль представляет собой кэш данных для RISC-V процессора с поддержкой:
- Кэшируемых и некэшируемых запросов
- Интерфейса AXI4 для работы с внешней памятью
- Поддержки операций инвалидации и writeback
- Пайплайнизированных запросов

## Параметры

| Параметр | Описание |
|----------|----------|
| AXI_ID | Идентификатор AXI |

## Входы и выходы

### Входные сигналы процессорного интерфейса

| Сигнал | Описание |
|--------|----------|
| clk_i | Тактовый сигнал |
| rst_i | Сигнал сброса |
| mem_addr_i[31:0] | Адрес памяти |
| mem_data_wr_i[31:0] | Данные для записи |
| mem_rd_i | Сигнал чтения |
| mem_wr_i[3:0] | Сигналы записи (по байтам) |
| mem_cacheable_i | Флаг кэшируемости доступа |
| mem_req_tag_i[10:0] | Тег запроса |
| mem_invalidate_i | Сигнал инвалидации кэша |
| mem_writeback_i | Сигнал сброса кэша в память |
| mem_flush_i | Сигнал полного сброса кэша |

### Входные сигналы AXI интерфейса

| Сигнал | Описание |
|--------|----------|
| axi_*ready_i | Сигналы готовности AXI |
| axi_*valid_i | Сигналы валидности данных AXI |
| axi_*data_i | Входные данные AXI |
| axi_*resp_i | Коды ответа AXI |

### Выходные сигналы процессорного интерфейса

| Сигнал | Описание |
|--------|----------|
| mem_data_rd_o[31:0] | Считанные данные |
| mem_accept_o | Подтверждение приема запроса |
| mem_ack_o | Подтверждение выполнения запроса |
| mem_error_o | Сигнал ошибки |
| mem_resp_tag_o[10:0] | Тег ответа |

### Выходные сигналы AXI интерфейса

| Сигнал | Описание |
|--------|----------|
| axi_*valid_o | Сигналы валидности AXI |
| axi_*addr_o | Адреса AXI |
| axi_*data_o | Выходные данные AXI |
| axi_*ready_o | Сигналы готовности AXI |

## Подключенные модули

Модуль состоит из 6

## Модуль dcache_if_pmem

### Назначение

Интерфейсный модуль между кэшем данных и внешней памятью, обеспечивающий:
- Буферизацию запросов на чтение/запись
- Управление потоком данных
- Согласование протоколов

### Ключевые особенности

1. **Двухканальная буферизация**:
   - Отдельные FIFO для запросов и ответов
   - Глубина буферов: 2 элемента каждый
   - Поддержка back-pressure

2. **Обработка транзакций**:
   - Поддержка 1 невыполненного запроса
   - Фильтрация служебных операций
   - Генерация сигналов подтверждения и ошибок

3. **Интерфейсная совместимость**:
   - Адаптация к протоколу AXI4/AXI4-Lite
   - Поддержка пакетных операций
   - Выравнивание адресов

### Основные функции

1. **Управление запросами**:
   - Прием запросов от кэша данных
   - Буферизация и маршрутизация
   - Формирование выходных сигналов

2. **Обработка ответов**:
   - Сопоставление тегов запросов/ответов
   - Передача данных и статусов обратно в кэш
   - Обработка ошибок доступа

3. **Служебные операции**:
   - Пропуск некритичных запросов
   - Отслеживание состояния выполнения
   - Синхронизация с тактовым сигналом

## Модуль dcache_pmem_mux

### Назначение

Мультиплексор интерфейса памяти кэша данных, обеспечивающий:
- Коммутацию между двумя источниками запросов к памяти
- Распределение ответов памяти соответствующим источникам
- Синхронизацию потоков данных

### Ключевые особенности

1. **Двухканальная коммутация**:
   - Выбор между inport0 и inport1 по сигналу select_i
   - Полная поддержка всех сигналов интерфейса памяти

2. **Синхронизация ответов**:
   - Фиксация состояния селектора для корреляции запросов/ответов
   - Задержка сигнала select на 1 такт для согласования фаз

3. **Прозрачная маршрутизация**:
   - Сквозная передача всех параметров запроса
   - Распределение ответов источнику

### Основные функции

1. **Мультиплексирование запросов**:
   - Выбор активного канала по select_i
   - Передача wr/rd сигналов
   - Маршрутизация адреса и данных записи

2. **Демультиплексирование ответов**:
   - Направление подтверждений соответствующему источнику
   - Распределение данных чтения и флагов ошибок

3. **Управление потоком**:
   - Передача сигналов готовности выбранному каналу
   - Синхронизация с тактовым сигналом
   - Обработка сброса

## Модуль dcache_mux

### Назначение

Мультиплексор доступа к кэшируемой и некэшируемой памяти, обеспечивающий:
- Маршрутизацию запросов в зависимости от типа памяти
- Контроль состояния выполнения операций
- Согласование интерфейсов кэшируемого и некэшируемого доступа

### Ключевые особенности

1. **Два порта**:
   - Кэшируемый доступ
   - Прямой доступ к памяти
   - Автоматический выбор на основе mem_cacheable_i

2. **Управление потоком**:
   - Отслеживание невыполненных запросов
   - Блокировка конфликтующих операций
   - Контроль перекрывающихся транзакций

3. **Синхронизация**:
   - Фиксация типа текущего доступа
   - Согласование тактовых доменов
   - Обработка сброса

### Основные функции

1. **Маршрутизация запросов**:
   - Распределение операций чтения/записи
   - Передача служебных команд
   - Переадресация тегов запросов

2. **Обработка ответов**:
   - Выбор источника данных для чтения
   - Маршрутизация подтверждений и ошибок
   - Возврат тегов ответов

3. **Контроль состояния**:
   - Отслеживание активных транзакций
   - Предотвращение конфликтов доступа
   - Индикация активного типа доступа

## Модуль dcache_axi

### Назначение
Адаптер интерфейса кэша данных к шине AXI, обеспечивающий:
- Преобразование протоколов
- Управление burst-транзакциями
- Буферизацию запросов и ответов

### Ключевые особенности

1. **Двунаправленная буферизация**:
   - FIFO для исходящих запросов
   - Трекинг невыполненных транзакций
   - Поддержка back-pressure

2. **Полная поддержка AXI**:
   - Все каналы AXI (чтение, запись, ответы)
   - Поддержка burst-операций
   - Обработка всех сигналов AXI

3. **Управление потоком**:
   - Контроль количества outstanding-транзакций
   - Счетчик оставшихся burst-операций
   - Маркировка последней операции в burst

### Основные функции
1. **Интерфейс с кэшем**:
   - Прием запросов чтения/записи
   - Возврат данных и статусов
   - Управление готовностью

2. **Генерация AXI-транзакций**:
   - Формирование заголовков AXI
   - Управление burst-операциями
   - Маршрутизация данных записи

3. **Обработка ответов**:
   - Прием подтверждений
   - Обработка ошибок
   - Сопоставление ответов с запросами

## Модуль dcache_core

### Назначение
Ядро кэша данных процессора с политикой write-back, выполняющее:
- Кэширование данных для ускорения доступа
- Управление согласованностью данных
- Обработку всех типов запросов к памяти

### Ключевые особенности

1. **Архитектура кэша**:
   - 2-канальная set-associative организация
   - Размер строки: 32 байта
   - Псевдослучайный алгоритм замещения

2. **Политики работы**:
   - Write-back с выделением строк при чтении/записи
   - Поддержка некэшируемых областей памяти
   - Пайплайнинг операций

3. **Состояния автомата**:
   - 11 состояний (LOOKUP, REFILL, EVICT и др.)
   - Сложная логика переходов между состояниями

### Основные функции

1. **Обработка запросов**:
   - Чтение/запись данных
   - Инвалидация строк
   - Полная очистка кэша (flush)
   - Принудительная запись (writeback)

2. **Управление кэшем**:
   - Поиск данных по тегам
   - Заполнение строк при промахах
   - Вытеснение "грязных" строк
   - Обновление метаданных

3. **Интерфейс с памятью**:
   - Генерация burst-транзакций
   - Обработка подтверждений
   - Контроль ошибок

### Особенности реализации
- Двойные порты для RAM тегов и данных
- Глубокая конвейеризация операций
- Механизмы предотвращения конфликтов
- Поддержка отладки