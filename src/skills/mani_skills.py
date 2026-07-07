# Mani Skills
# Herramientas exclusivas del Tester y QA

def generate_test_report(tests_passed: int, tests_failed: int, bugs_found: list) -> dict:
    """Genera un reporte de calidad estructurado con evaluación de severidad."""
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
    
    status = "APPROVED" if pass_rate == 100 and len(bugs_found) == 0 else "REJECTED"
    
    report = {
        "status": status,
        "metrics": {
            "total_tests": total_tests,
            "passed": tests_passed,
            "failed": tests_failed,
            "pass_rate_percentage": round(pass_rate, 2)
        },
        "bugs": bugs_found
    }
    return report

def mock_run_unit_tests(test_file: str) -> dict:
    """Simula la ejecución de pruebas unitarias (Caja Blanca)."""
    # En la realidad esto usaría pytest o jest
    print(f"[Mani-Skill] Ejecutando suite de pruebas en: {test_file}")
    return {"passed": 5, "failed": 0, "errors": []}
