# Транскрайбер

## Описание

Для обработки текстов используется [Whisper](https://openai.com/research/whisper) от компании _OpenAI_ по ссылке паперы и прочая научная история с описанием принципа работы

Для работы приложения потребуется предобученная модель, выбранная скачается автоматически после запуска.

## Описание моделей

Ниже приведены типы моделей, с их примерным потреблением памяти и скоростью работы

|   Size   | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
| :------: | :--------: | :----------------: | :----------------: | :-----------: | :------------: |
|   tiny   |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|   base   |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
|  small   |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
|  medium  |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
|  large   |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
| large-v2 |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

## Установка и запуск (Hard Way)

- Устновить [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) для _Windows/Linux_ машин или [OrbStack](https://orbstack.dev) ну или любой любимый container runtime для _MacOS_ машин любым удобным для вас способом
- Открыть терминал в корне этой папки
- Ввести команду `docker compose up` (У вас может установиться более старая версия докера, в таком случае комманда может выглядеть `docker-compose up`)
- Дождаться строки *Application started*
- Открыть приложение по ссылке [Web](http://localhost)
- Готово! Вы даже великолепнее чем те, кто выбрал easy way!

## Установка и запуск (Easy Way only MacOS)

- В файле `docker-compose.yml` найти строчку *ASR_MODEL=tiny* и заменить *tiny* на любую понравившуюся модель.
- Запустить скрипт `run.sh` в папке двойным кликом _(Вероятнее всего потребуется ввести пароль Администратора)_
- Открыть приложение по ссылке [Web](http://localhost)
- Готово! Вы великолепны!
- После завершения работы, необходимо выполнить `stop.sh`
