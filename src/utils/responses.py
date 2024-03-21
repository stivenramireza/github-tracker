import json


class HttpResponse:
    status_code: int
    body: dict

    def __init__(self, status_code: int, body: dict) -> None:
        self.status_code = status_code
        self.body = body

    def to_dict(self) -> dict:
        return {
            'statusCode': self.status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': (
                json.dumps(self.body)
                if isinstance(self.body, dict)
                else json.dumps({'message': self.body})
            ),
        }


class OkResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(200, body)


class CreatedResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(201, body)


class BadRequestResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(400, body)


class UnauthorizedResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(401, body)


class ForbiddenResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(403, body)


class NotFoundResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(404, body)


class ConflictResponse(HttpResponse):

    def __init__(self, body: str | dict) -> None:
        super().__init__(409, body)


class InternalServerErrorResponse(HttpResponse):

    def __init__(self) -> None:
        super().__init__(500, 'Internal server error')
