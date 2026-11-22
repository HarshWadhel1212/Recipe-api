SAMPLE = {
    "title": "Pancakes",
    "description": "Fluffy breakfast pancakes",
    "instructions": "Mix everything. Fry on a pan.",
    "category": "Breakfast",
    "prep_time_minutes": 10,
    "cook_time_minutes": 15,
    "servings": 4,
    "ingredients": [
        {"name": "Flour", "quantity": "2 cups"},
        {"name": "Milk", "quantity": "1 cup"},
    ],
}


def create(client, **changes):
    return client.post("/recipes", json={**SAMPLE, **changes})


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_recipe(client):
    r = create(client)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 1
    assert body["title"] == "Pancakes"
    assert len(body["ingredients"]) == 2


def test_create_recipe_invalid_data(client):
    r = create(client, title="", servings=0)
    assert r.status_code == 422  # validation error


def test_get_recipe(client):
    create(client)
    r = client.get("/recipes/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Pancakes"


def test_get_recipe_not_found(client):
    r = client.get("/recipes/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Recipe not found"


def test_list_search_filter_and_pagination(client):
    create(client, title="Pancakes", category="Breakfast")
    create(client, title="Pasta", category="Dinner")
    create(client, title="Omelette", category="Breakfast")

    assert len(client.get("/recipes").json()) == 3
    assert len(client.get("/recipes", params={"category": "breakfast"}).json()) == 2
    assert [x["title"] for x in client.get("/recipes", params={"search": "pas"}).json()] == ["Pasta"]
    assert len(client.get("/recipes", params={"limit": 2}).json()) == 2
    assert len(client.get("/recipes", params={"skip": 2}).json()) == 1


def test_update_recipe_partial(client):
    create(client)
    r = client.put("/recipes/1", json={"title": "Banana Pancakes"})
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Banana Pancakes"
    assert body["servings"] == 4  # unchanged
    assert len(body["ingredients"]) == 2  # unchanged


def test_update_replaces_ingredients(client):
    create(client)
    r = client.put("/recipes/1", json={"ingredients": [{"name": "Banana", "quantity": "2"}]})
    assert [i["name"] for i in r.json()["ingredients"]] == ["Banana"]


def test_update_not_found(client):
    assert client.put("/recipes/999", json={"title": "X"}).status_code == 404


def test_delete_recipe(client):
    create(client)
    assert client.delete("/recipes/1").status_code == 204
    assert client.get("/recipes/1").status_code == 404
