import psycopg2


def create_db():
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
            CREATE TABLE student (
                id serial PRIMARY KEY,
                name character varying(100),
                gpa numeric(10,2),
                birth timestamp with time zone
            )
            """)

            curs.execute("""
            CREATE TABLE course (
                id serial PRIMARY KEY,
                name character varying(100)
            )
            """)

            curs.execute("""
            CREATE TABLE student_course(
                id serial PRIMARY KEY,
                student_id INTEGER REFERENCES student(id),
                course_id INTEGER REFERENCES course(id)
            )
            """)


def get_students(course_id):
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
            SELECT student.id, student.name, course.name FROM student_course 
            JOIN student on student.id = student_course.student_id 
            JOIN course on course.id = student_course.course_id where course_id = %s
            """, (course_id['course_number']))
            student_data = curs.fetchall()
            print(student_data)


def add_students(course_id, students):
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
            INSERT INTO student VALUES (default, %s, %s, %s)
            """, (students['name'], students['gpa'], students['birth'])
            )

            curs.execute("""
            SELECT ID FROM STUDENT WHERE NAME = %s
            """, (students['name'],)
            )
            data = curs.fetchall()

            curs.execute("""
            INSERT INTO student_course VALUES (default, %s, %s)
            """, (data[0], course_id)
            )


def add_student(student):
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO student VALUES (%s, %s, %s)
                """, (student['name'], student['gpa'], student['birth'])
                )


def get_student(student_id):
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
            SELECT * FROM student WHERE id = {0}
            """.format(student_id)
            )
            student_data = curs.fetchall()
            print(student_data[0])


def course_creation(name_course):
    with psycopg2.connect(dbname='homework_8_0', user='postgres', password='210576') as conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO course VALUES (default, %s)
                """, (name_course['name'],)
                )


def main():
    command = input('Введите команду: ' + '\n' +
                   '1 - создание таблиц базы данных' + '\n' +
                   '2 - создать нового студента и записать его на курс' + '\n' +
                   '3 - вывести список студентов конкретного курса' + '\n' +
                   '4 - создать нового студента без записи на курс' + '\n' +
                   '5 - вывести данные студента по номеру ID' + '\n' +
                   '6 - создать новый курс (ввести название)' + '\n' + ': ')
    if command == '1':
        try:
            create_db()
        except psycopg2.errors.DuplicateTable:
            print('Таблицы базы данных уже созданы!')

    elif command == '2':
        name = input('Введите Имя и Фамилию студента через пробел: ')
        birth = input('Введите дату рождения в формате ГГГГ-ММ-ДД: ')
        gpa = input('Введите средний балл аттестата в формате 10.2(через точку): ')
        course = input('Введите номер курса, например 1: ')
        new_student = {'name': name, 'gpa': gpa, 'birth': birth}
        add_students(course, new_student)

    elif command == '3':
        course_number = input('Введите номер курса, например 1: ')
        course_number = {'course_number': course_number}
        get_students(course_number)

    elif command == '4':
        name = input('Введите Имя и Фамилию студента через пробел: ')
        birth = input('Введите дату рождения в формате ГГГГ-ММ-ДД: ')
        gpa = input('Введите средний балл аттестата в формате 10.2(через точку): ')
        new_student = {'name': name, 'gpa': gpa, 'birth': birth}
        add_student(new_student)

    elif command == '5':
        try:
            student_id = input('Введите ID студента, например 1: ')
            get_student(student_id)
        except IndexError:
            print('С таким индексом студента нет!')

    elif command == '6':
        name_course = input('Введите название курса: ')
        new_course = {'name': name_course}
        course_creation(new_course)


if __name__ == "__main__":

    main()
