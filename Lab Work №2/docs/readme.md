# Сервис для поиска пропавших домашних животных

## Диаграмма системного контекста

![context-diagram](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/Context_diagram.drawio.png)

## Диаграмма контейнеров
Я выбрал Микросервисную архитектуру в качестве архитектурного стиля. Это решение позволит мне эффективно разделить нагрузку между разными сервисами. Благодаря этому, каждый сервис сможет разрабатываться и настраиваться независимо от других, а также разворачиваться отдельно.
![component-diagram](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/Component_diagram.drawio.png)

## Диаграмма компонентов

### API Пользователя
![component-diagram-user](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/API%20%D0%9F%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F.drawio.png)

### API Администратора

![component-diagram-worker](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/API_Administrator.drawio.png)

### API Рекламодатель

![component-diagram-advertiser](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/API_Advertiser.drawio.png)

### API Модератор

![component-diagram-moderator](https://github.com/nikitasik4ik/HSE_Architecture/blob/LabWork2/Lab%20Work%20%E2%84%962/docs/API%20Moderator.drawio.png)
