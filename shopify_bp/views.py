from flask import Blueprint, render_template, current_app, request, url_for, session, redirect
import shopify
from app import db
from shopify_bp.models import Shop
from shopify_bp.utils import shopify_auth_required

shopify_bp = Blueprint('shopify_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/shopify')

@shopify_bp.route('/')
@shopify_auth_required
def index():
    """ Render the index page of our application.
    """

    return render_template('index.html')

@shopify_bp.route('/install')
def install():
    shop_url = request.args.get("shop")
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET']
    )
    session = shopify.Session(shop_url, version='2019-04')

    scope=[
        "write_products", "read_products", "read_script_tags", 
        "write_script_tags"
    ]
    permission_url = session.create_permission_url(
        scope, url_for("shopify_bp.finalize", _external=True)
    )

    return render_template('install.html', permission_url=permission_url)
    # return redirect(permission_url)

@shopify_bp.route('/finalize')
def finalize():
    """ Generate shop token and store the shop information.
    
    """
    
    shop_url = request.args.get("shop")
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])
    shopify_session = shopify.Session(shop_url, version='2019-04')

    token = shopify_session.request_token(request.args)

    shop = Shop(shop=shop_url, token=token)
    db.session.add(shop)
    db.session.commit()

    session['shopify_url'] = shop_url
    session['shopify_token'] = token
    session['shopify_id'] = shop.id


    return redirect(url_for('shopify_bp.index'))