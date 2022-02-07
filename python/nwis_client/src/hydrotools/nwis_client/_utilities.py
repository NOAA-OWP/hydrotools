from functools import wraps, partial
import inspect
from inspect import Parameter
import warnings

# typing imports
from typing import Callable, Optional


def get_varkeyword_arg(fn: Callable) -> Optional[str]:
    """Return name of a callable's variadic keyword argument (idiomatically kwargs) if it exists."""
    sig = inspect.signature(fn)
    sig_params = sig.parameters.values()

    if len(sig_params) > 0:
        # var kwargs have to be last parameter in python func signatures
        last_param = next(reversed(sig_params))

        if last_param.kind is Parameter.VAR_KEYWORD:
            return last_param.name

    return None


def verify_case_insensitive_kwargs(
    fn: Optional[Callable] = None,
    *,
    handler: Callable[[str], None] = partial(warnings.warn, category=RuntimeWarning),
) -> Callable:
    """Verify that variadic keyword argument names do not colide with positional, keyword, or
    keyword only arguments when case is ignored. By default, a RuntimeWarning is thrown if an
    argument and variadic keyword argument are case insensitively equal. Change the behavior using
    the `handler` parameter.

    Example:

    ```python
    from functools import partial

    def raise_exception(e: Exception, s: str) -> None:
        raise e(s)

    # raise `RuntimeError` instead of throwing `RuntimeWarning`
    @verify_case_insensitive_kwargs(handler=partial(raise_exception, RuntimeError))
    def fn(a: int, **kwargs) -> None:
        ...
    ```
    """

    def outer(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            signature = inspect.signature(fn)

            # this only applies to callables that have variadic keyword args
            variadic_keyword_arg_name = get_varkeyword_arg(fn)

            # filter callable parameters to positional or keyword only parameters
            keyword_non_kwargs = {
                arg.name.lower(): arg.name
                for arg in signature.parameters.values()
                if arg.kind
                in (
                    Parameter.POSITIONAL_OR_KEYWORD,
                    Parameter.KEYWORD_ONLY,
                )
            }

            # early return if no variadic keyword arguments present
            if variadic_keyword_arg_name is None:
                return fn(*args, **kwargs)

            bound_params = signature.bind(*args, **kwargs)

            variadic_keyword_args = bound_params.arguments.get(variadic_keyword_arg_name, dict())

            errors = []  # type: List[Tuple[str, str]]
            for kwarg in variadic_keyword_args.keys():
                lowered_kwarg = kwarg.lower()

                if lowered_kwarg in keyword_non_kwargs:
                    errors.append((keyword_non_kwargs[lowered_kwarg], kwarg))

            if errors:
                error_message = f"{fn.__name__}() provided potentially case ambiguous kwarg parameter."
                for e in errors:
                    error_message += (
                        f"\nfunction parameter, {e[0]!r}, provided as {e[1]!r}"
                    )

                handler(error_message)

            return fn(*args, **kwargs)

        return wrapper

    if fn is not None:
        return outer(fn)

    return outer
