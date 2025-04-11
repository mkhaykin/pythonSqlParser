import os
from typing import List, Set, Tuple

import sqlglot


def get_tables_from_expression(sql_exp: sqlglot.Expression) -> Set[str]:
    """
    Выбирает из разобранного запроса реальные таблицы.
    Возвращает множество имен таблиц в запросе.
    """
    cte_names = {cte.alias_or_name.lower() for cte in sql_exp.find_all(sqlglot.exp.CTE)}

    # таблицы без cte
    real_tables = set()
    for table in sql_exp.find_all(sqlglot.exp.Table):
        name = table.name
        schema = table.args.get("db")
        if name.lower() not in cte_names:
            real_tables.add(f"{schema}.{name}" if schema else name)

    return real_tables


def analyze_sql_file_content(sql_content: str) -> Set[str]:
    """
    Анализирует текст валидного sql запроса(ов).
    Возвращает множество имен таблиц в запросе.
    """
    result = set()
    expressions = sqlglot.parse(sql_content)
    for expr in expressions:
        if expr:
            result.update(get_tables_from_expression(expr))

    return result


def analyze_sql_files(directory: str) -> List[Tuple[str, List[str]]]:
    """
    Анализирует все SQL-файлы в указанном каталоге и его подкаталогах.
    Возвращает список кортежей (имя_файла, [список_таблиц]).
    """
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".sql"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding="utf-8") as f:
                        sql_content = f.read()
                    results.append(
                        (
                            file_path,
                            sorted(analyze_sql_file_content(sql_content)),
                        ),
                    )
                except Exception as e:
                    print(f"Ошибка при обработке файла {file_path}: {str(e)}")

    return results


def main() -> None:
    results = analyze_sql_files("./samples/")
    for file_path, tables in results:
        print(f"{file_path}: {tables}")


if __name__ == "__main__":
    main()
