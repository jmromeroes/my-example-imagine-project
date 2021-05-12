all:
	@echo "Available commands: \n\
		make install : to install poetry and other dependent packages \n\
		make adminuser : creates a superuser to access the django admin \n\
		make dev : runs django development server \n\
		make run : run the django application \n\
		make shell : start a poetry shell with all required packages available in the environment \n\
		make lint : runs linters on all project files and shows the changes \n\
		make test : run the test suite  \n\
		make coverage : runs tests and creates a report of the coverage \n\
	"

install:
	python3 -m pip install poetry
	poetry install
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev:
	poetry run python manage.py runserver

run: install
	# the default settings file is development, it can be changed
	# for any of the others, please don't use development setting in production
	export DJANGO_SETTINGS_MODULE='project.settings';\
	poetry run gunicorn project.wsgi:application --bind localhost:8000

shell:
	@echo 'Starting poetry shell. Press Ctrl-d to exit from the shell'
	poetry shell

lint:
	# starts a poetry shell, shows autopep8 diff and then fixes the files
	# does the same for isort
	@echo '---Running autopep8---'
	poetry run autopep8 my_example_imagine_project -r -d
	poetry run autopep8 my_example_imagine_project -r -i
	@echo '---Running isort---'
	poetry run isort my_example_imagine_project --diff
	poetry run isort my_example_imagine_project --atomic

coverage:
	@echo 'Running tests and making coverage files'
	poetry run coverage run manage.py test
	poetry run coverage report
	poetry run coverage html
	@echo 'to see the complete report, open ./htmlcov/index.html on the htmlcov folder'

adminuser:
	@echo 'creating Django admin user'
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
	User.objects.create_superuser('admin', '', '$(password)')" \
	| poetry run python manage.py shell
	@echo 'Username: admin , Password: $(password)'

test:
	@echo 'Running tests'
	poetry run python manage.py test
