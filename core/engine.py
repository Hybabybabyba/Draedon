import importlib
import importlib.util
import inspect
from pathlib import Path
from core.base_module import base_module, module_result
from core.storage import Storage

MODULES_DIR = Path(__file__).parent.parent / "modules"

class Engine:
    def __init__(self):
        self.storage = Storage()
        self.modules: dict[str, base_module] = {}
        self._load_modules()

    def _load_modules(self):
        for filepath in MODULES_DIR.glob("py_*.py"):
            module_name = filepath.stem  
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, filepath
                )
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(cls, base_module) and cls is not base_module:
                        instance = cls()
                        self.modules[instance.name] = instance
                        print(f"[+] Module has been loaded: {instance.name}")
                        break

            except Exception as e:
                print(f"[!] Load Error {module_name}: {e}")

    def run(self, target: str, target_type: str = "ip") -> list[module_result]:
        results = []
        eligible = [
            m for m in self.modules.values()
            if m.can_handle(target_type)
        ]

        if not eligible:
            print(f"[!] No modules for this mission: {target_type}")
            return results

        print(f"\n Target: {target} ({target_type})")
        print(f" Modules to execute: {len(eligible)}\n")

        for module in eligible:
            print(f"  >> {module.name}...")
            try:
                result = module.run(target)
                self.storage.save(result)
                results.append(result)
                status = "OK" if result.success else f"FAIL: {result.error}"
                print(f"  << {module.name}: {status}")
            except Exception as e:
                print(f"  << {module.name}: EXCEPTION: {e}")

        return results

    def list_modules(self):
        print("\n Loaded modules:")
        for name, mod in self.modules.items():
            types = ", ".join(mod.accepts)
            print(f"  · {name:<20} {mod.description} [{types}]")