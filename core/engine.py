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
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(cls, base_module) and cls is not base_module:
                        instance = cls()
                        self.modules[instance.name] = instance
                        print(f"[+] Module loaded: {instance.name}")
                        break
            except Exception as e:
                print(f"[!] Load error {module_name}: {e}")

    def run_smart(self, target: str, target_type: str) -> list[module_result]:
        results = []
        for module in self.modules.values():
            if not module.can_handle(target_type):
                continue
            try:
                result = module.run(target)
            except Exception as e:
                result = module_result(
                    module_name=module.name,
                    target=target,
                    success=False,
                    result_data={},
                    error=str(e),
                )
            self.storage.save(result)
            results.append(result)
        return results

    def run_manual(self, target: str, selected_names: list[str]) -> list[module_result]:
        results = []
        for name in selected_names:
            module = self.modules.get(name)
            if not module:
                continue
            try:
                result = module.run(target)
            except Exception as e:
                result = module_result(
                    module_name=module.name,
                    target=target,
                    success=False,
                    result_data={},
                    error=str(e),
                )
            self.storage.save(result)
            results.append(result)
        return results

    def list_modules(self):
        print("\n Loaded modules:")
        for name, mod in self.modules.items():
            types = ", ".join(mod.supported_types)
            print(f"  · {name:<20} {mod.description} [{types}]")
