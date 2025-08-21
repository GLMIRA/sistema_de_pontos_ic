import time
import sys
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command para aguardar o banco de dados"""

    help = "Aguarda o banco de dados ficar disponível"

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout", type=int, default=60, help="Timeout em segundos (padrão: 60)"
        )

    def handle(self, *args, **options):
        """Aguarda o banco ficar disponível"""
        timeout = options["timeout"]
        start_time = time.time()

        self.stdout.write("Aguardando banco de dados...")

        db_conn = None
        while not db_conn:
            try:
                # Tenta conectar no banco
                db_conn = connections["default"]
                db_conn.cursor()

            except OperationalError:
                # Se não conseguir conectar, verifica timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    self.stdout.write(
                        self.style.ERROR(
                            f"❌ Timeout de {timeout}s atingido! Banco não disponível."
                        )
                    )
                    sys.exit(1)

                self.stdout.write(
                    "🔄 Banco não disponível, tentando novamente em 2s..."
                )
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("✅ Banco de dados disponível!"))
