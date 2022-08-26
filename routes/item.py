from unicodedata import category
from flask import Blueprint, jsonify, request
from data import Item, Tag, User, Category
import flask
from main import db
from routes.decorators import require_auth

item_blueprint = Blueprint('item', __name__, url_prefix='/item')

@item_blueprint.route('/categories', methods=['GET'])
def get_categories():
    """
    [REST GET] /item/tags
    Returns all tags in the database

    Parameters:
        lang (str): Language to return tags in. [en, nl]

    Example:
    {
        "tags": [
            {
                "id": 1,
                "name": "Voedsel"
            },
            ...
        ]
    }
    """
    # //TODO: Make language return in the same json format
    try:
        language = request.args.get('lang')
        if language is None:
            language = 'en'
        # select column name, name_en, name_nl from tag
        if language == 'en':
            tags = Category.query.with_entities(Category.id, Category.name_en).all()
        elif language == 'nl':
            tags = Category.query.with_entities(Category.id, Category.name_nl).all()
        else:
            return jsonify({"error": "Invalid language"}), 400
        return jsonify(tags), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_blueprint.route('/tags', methods=['GET'])
def get_tags():
    """
    [REST GET] /item/tags
    Returns all tags in the database

    Parameters:
        lang (str): Language to return tags in. [en, nl]

    Example:
    {
        "tags": [
            {
                "id": 1,
                "name": "tag1"
            },
            ...
        ]
    }
    """
    # //TODO: Make language return in the same json format
    try:
        language = request.args.get('lang')
        if language is None:
            language = 'en'
        # select column name, name_en, name_nl from tag
        if language == 'en':
            tags = Tag.query.with_entities(Tag.id, Tag.name_en).all()
        elif language == 'nl':
            tags = Tag.query.with_entities(Tag.id, Tag.name_nl).all()
        else:
            return jsonify({"error": "Invalid language"}), 400
        return jsonify(tags), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_blueprint.route('/add', methods=['POST'])
@require_auth()
def add_item(user: User):
    """
    [REST POST] /item/add
    Adds an item to the database
    Requires authentication
    
    Example request:
    {
        auth: <token>,
        name: "Carrots",
        description: "900 grams of carrots",
        image: <base64 imagedata>,
        expiry_in_days: 5,
        tags: [1, 2, 3]
        category: 1
    }
    """
    try:
        request_data = flask.request.get_json()
        item = Item(
            user=user, 
            name=request_data['name'], 
            description=request_data['description'],
            image=request_data['image'],
            expiry_in_days=request_data['expiry_in_days'],
            category=Category.query.filter_by(id=request_data['category']).first(),
            tags = Tag.query.filter(Tag.id.in_(request_data['tags'])).all()
        )
        db.session.add(item)
        db.session.commit()
        return jsonify("Item added"), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_blueprint.route('/edit', methods=['POST'])
@require_auth()
def edit_item(user: User):
    request_data = flask.request.get_json()
    item = Item.get(request_data['id'])
    if item is None:
        return flask.jsonify({"error": "Item not found"}), 404
    if item.user != user:
        return flask.jsonify({"error": "You are not allowed to edit this item"}), 403

@item_blueprint.route('/list', methods=['POST'])
def list_items():
    """
    [REST GET] /item/list
    Lists the items.
    No authentication required.

    Parameters:
        length (int): Amount of items to return.
        offset (int): Offset of the items to return.
        sort (str): Sort order. [asc, desc]
        filter (list[int]): Filter by tags
        category (int): Filter by category
        order_by (str): Order by field. [expiry_in_days, created_at]

    Example:
    {
        "items": [
            {
                "id": 1,
                "user_id": 1,
                "name": "Carrots",
                "description": "900 grams of carrots",
                "image": <base64 imagedata>,
                "created_at": "2020-01-01",
                "expiry_in_days": 5,
                "tags": [1, 2, 3]
                "category": 1
            },
            ...
        ]
    }
    """
    request_data = flask.request.get_json()
    try:
        length = int(request_data.get('length', 20))
        offset = int(request_data.get('offset', 0))
        sort = request_data.get('sort', 'asc')
        filter = request_data.getlist('filter')
        category = request_data.get('category')
        order_by = request_data.get('order_by', 'expiry_in_days')
        if sort not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort order"}), 400
        if order_by not in ['expiry_in_days', 'created_at']:
            return jsonify({"error": "Invalid order by field"}), 400
        if category is not None:
            category = Category.query.filter_by(id=category).first()
            if category is None:
                return jsonify({"error": "Invalid category"}), 400
            items = Item.query.filter_by(category=category).all()
        else:
            items = Item.query.all()
        if filter is not None:
            filter = [int(tag) for tag in filter]
            items = [item for item in items if any(tag in item.tags for tag in filter)]
        if sort == 'asc':
            items = sorted(items, key=lambda item: getattr(item, order_by))
        else:
            items = sorted(items, key=lambda item: getattr(item, order_by), reverse=True)
        items = items[offset:offset+length]
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
