import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import NumberRange
import re

import configparser
import MySQLdb
from secrets import token_hex

app = Flask(__name__, static_folder='static', template_folder='templates')
db_config = configparser.ConfigParser()
db_config.read('config.ini')

app.secret_key = token_hex(16)

# Initialize database
db = MySQLdb.connect(host=db_config.get('Database', 'host'),
                        user=db_config.get('Database', 'user'),
                        password=db_config.get('Database', 'password'),
                        port=int(db_config.get('Database', 'port')))

char_db = db_config.get('Database', 'char_database')
world_db = db_config.get('Database', 'world_database')

@app.route('/')
def index():

    return(render_template('index.html'))

@app.route('/conf_editor', methods=['GET', 'POST'])
def conf_editor():
    form = AHBotConfigForm(request.form)
    config = read_config()
    if request.method == 'POST' and form.validate():
        # Save form data to config file
        config['AuctionHouseBot.CharacterName'] = '"' + form.character_name.data + '"'
        config['AuctionHouseBot.Seller.Enabled'] = int(form.seller_enabled.data)
        config['AuctionHouseBot.DEBUG.Seller'] = int(form.seller_debug.data)
        config['AuctionHouseBot.Alliance.Items.Amount.Ratio'] = form.alliance_ratio.data
        config['AuctionHouseBot.Horde.Items.Amount.Ratio'] = form.horde_ratio.data
        config['AuctionHouseBot.Neutral.Items.Amount.Ratio'] = form.neutral_ratio.data
        config['AuctionHouseBot.MinTime'] = form.mintime.data
        config['AuctionHouseBot.MaxTime'] = form.maxtime.data
        config['AuctionHouseBot.Items.Vendor'] = int(form.items_vendor.data)
        config['AuctionHouseBot.Items.Loot'] = int(form.items_loot.data)
        config['AuctionHouseBot.Items.Misc'] = int(form.items_misc.data)
        config['AuctionHouseBot.Bind.No'] = int(form.bind_no.data)
        config['AuctionHouseBot.Bind.Pickup'] = int(form.bind_pickup.data)
        config['AuctionHouseBot.Bind.Equip'] = int(form.bind_equip.data)
        config['AuctionHouseBot.Bind.Use'] = int(form.bind_use.data)
        config['AuctionHouseBot.Bind.Quest'] = int(form.bind_quest.data)
        config['AuctionHouseBot.LockBox.Enabled'] = int(form.lockbox_enabled.data)
        config['AuctionHouseBot.ItemsPerCycle.Boost'] = form.itemspercycle_boost.data
        config['AuctionHouseBot.ItemsPerCycle.Normal'] = form.itemspercycle_normal.data
        config['AuctionHouseBot.BuyPrice.Seller'] = int(form.buyprice_seller.data)
        config['AuctionHouseBot.Alliance.Price.Ratio'] = form.alliance_price_ratio.data
        config['AuctionHouseBot.Horde.Price.Ratio'] = form.horde_price_ratio.data
        config['AuctionHouseBot.Neutral.Price.Ratio'] = form.neutral_price_ratio.data
        config['AuctionHouseBot.Items.ItemLevel.Min'] = form.items_itemlevel_min.data
        config['AuctionHouseBot.Items.ItemLevel.Max'] = form.items_itemlevel_max.data
        config['AuctionHouseBot.Items.ReqLevel.Min'] = form.items_reqlevel_min.data
        config['AuctionHouseBot.Items.ReqLevel.Max'] = form.items_reqlevel_max.data
        config['AuctionHouseBot.Items.ReqSkill.Min'] = form.items_reqskill_min.data
        config['AuctionHouseBot.Items.ReqSkill.Max'] = form.items_reqskill_max.data
        config['AuctionHouseBot.Items.Amount.Grey'] = form.items_amount_grey.data
        config['AuctionHouseBot.Items.Amount.White'] = form.items_amount_white.data
        config['AuctionHouseBot.Items.Amount.Green'] = form.items_amount_green.data
        config['AuctionHouseBot.Items.Amount.Blue'] = form.items_amount_blue.data
        config['AuctionHouseBot.Items.Amount.Purple'] = form.items_amount_purple.data
        config['AuctionHouseBot.Items.Amount.Orange'] = form.items_amount_orange.data
        config['AuctionHouseBot.Items.Amount.Yellow'] = form.items_amount_yellow.data
        config['AuctionHouseBot.Class.Consumable'] = form.class_consumable.data
        config['AuctionHouseBot.Class.Container'] = form.class_container.data
        config['AuctionHouseBot.Class.Weapon'] = form.class_weapon.data
        config['AuctionHouseBot.Class.Gem'] = form.class_gem.data
        config['AuctionHouseBot.Class.Armor'] = form.class_armor.data
        config['AuctionHouseBot.Class.Reagent'] = form.class_reagent.data
        config['AuctionHouseBot.Class.Projectile'] = form.class_projectile.data
        config['AuctionHouseBot.Class.TradeGood'] = form.class_tradegood.data
        config['AuctionHouseBot.Class.Generic'] = form.class_generic.data
        config['AuctionHouseBot.Class.Recipe'] = form.class_recipe.data
        config['AuctionHouseBot.Class.Quiver'] = form.class_quiver.data
        config['AuctionHouseBot.Class.Quest'] = form.class_quest.data
        config['AuctionHouseBot.Class.Key'] = form.class_key.data
        config['AuctionHouseBot.Class.Misc'] = form.class_misc.data
        config['AuctionHouseBot.Class.Glyph'] = form.class_glyph.data
        config['AuctionHouseBot.Class.Misc.Mount.ReqLevel.Min'] = form.class_misc_mount_reqlevel_min.data
        config['AuctionHouseBot.Class.Misc.Mount.ReqLevel.Max'] = form.class_misc_mount_reqlevel_max.data
        config['AuctionHouseBot.Class.Misc.Mount.ReqSkill.Min'] = form.class_misc_mount_reqskill_min.data
        config['AuctionHouseBot.Class.Misc.Mount.ReqSkill.Max'] = form.class_misc_mount_reqskill_max.data
        config['AuctionHouseBot.Class.Glyph.ReqLevel.Min'] = form.class_glyph_reqlevel_min.data
        config['AuctionHouseBot.Class.Glyph.ReqLevel.Max'] = form.class_glyph_reqlevel_max.data
        config['AuctionHouseBot.Class.Glyph.ItemLevel.Min'] = form.class_glyph_itemlevel_min.data
        config['AuctionHouseBot.Class.Glyph.ItemLevel.Max'] = form.class_glyph_itemlevel_max.data
        config['AuctionHouseBot.Class.TradeGood.ItemLevel.Min'] = form.class_tradegood_itemlevel_min.data
        config['AuctionHouseBot.Class.TradeGood.ItemLevel.Max'] = form.class_tradegood_itemlevel_max.data
        config['AuctionHouseBot.Class.Container.ItemLevel.Min'] = form.class_container_itemlevel_min.data
        config['AuctionHouseBot.Class.Container.ItemLevel.Max'] = form.class_container_itemlevel_max.data
        config['AuctionHouseBot.forceIncludeItems'] = '"' + form.force_include_items.data + '"'
        config['AuctionHouseBot.forceExcludeItems'] = '"' + form.force_exclude_items.data + '"'
        config['AuctionHouseBot.Buyer.Enabled'] = int(form.buyer_enabled.data)
        config['AuctionHouseBot.DEBUG.Buyer'] = int(form.buyer_debug.data)
        config['AuctionHouseBot.Buyer.Alliance.Enabled'] = int(form.buyer_alliance_enabled.data)
        config['AuctionHouseBot.Buyer.Horde.Enabled'] = int(form.buyer_horde_enabled.data)
        config['AuctionHouseBot.Buyer.Neutral.Enabled'] = int(form.buyer_neutral_enabled.data)
        config['AuctionHouseBot.Buyer.BuyPrice'] = int(form.buyer_buyprice.data)
        config['AuctionHouseBot.Buyer.Recheck.Interval'] = form.buyer_recheck_interval.data
        config['AuctionHouseBot.Buyer.Alliance.Chance.Ratio'] = form.buyer_alliance_chance_ratio.data
        config['AuctionHouseBot.Buyer.Horde.Chance.Ratio'] = form.buyer_horde_chance_ratio.data
        config['AuctionHouseBot.Buyer.Neutral.Chance.Ratio'] = form.buyer_neutral_chance_ratio.data

        write_config(config)
        return redirect(url_for('conf_editor'))
    else:
        form.character_name.data = config.get('AuctionHouseBot.CharacterName').strip('"')
        form.seller_enabled.data = bool(int(config.get('AuctionHouseBot.Seller.Enabled', 0)))
        form.seller_debug.data = bool(int(config.get('AuctionHouseBot.DEBUG.Seller', 0)))
        form.alliance_ratio.data = config.get('AuctionHouseBot.Alliance.Items.Amount.Ratio')
        form.horde_ratio.data = config.get('AuctionHouseBot.Horde.Items.Amount.Ratio')
        form.neutral_ratio.data = config.get('AuctionHouseBot.Neutral.Items.Amount.Ratio')
        form.mintime.data = config.get('AuctionHouseBot.MinTime', 1)
        form.maxtime.data = config.get('AuctionHouseBot.MaxTime', 72)
        form.items_vendor.data = bool(int(config.get('AuctionHouseBot.Items.Vendor', 0)))
        form.items_loot.data = bool(int(config.get('AuctionHouseBot.Items.Loot', 0)))
        form.items_misc.data = bool(int(config.get('AuctionHouseBot.Items.Misc', 0)))
        form.bind_no.data = bool(int(config.get('AuctionHouseBot.Bind.No', 0)))
        form.bind_pickup.data = bool(int(config.get('AuctionHouseBot.Bind.Pickup', 0)))
        form.bind_equip.data = bool(int(config.get('AuctionHouseBot.Bind.Equip', 0)))
        form.bind_use.data = bool(int(config.get('AuctionHouseBot.Bind.Use', 0)))
        form.bind_quest.data = bool(int(config.get('AuctionHouseBot.Bind.Quest', 0)))
        form.lockbox_enabled.data = bool(int(config.get('AuctionHouseBot.LockBox.Enabled', 0)))
        form.itemspercycle_boost.data = int(config.get('AuctionHouseBot.ItemsPerCycle.Boost', 75))
        form.itemspercycle_normal.data = int(config.get('AuctionHouseBot.ItemsPerCycle.Normal', 20))
        form.buyprice_seller.data = int(config.get('AuctionHouseBot.BuyPrice.Seller', 1))
        form.alliance_price_ratio.data = int(config.get('AuctionHouseBot.Alliance.Price.Ratio', 200))
        form.horde_price_ratio.data = int(config.get('AuctionHouseBot.Horde.Price.Ratio', 200))
        form.neutral_price_ratio.data = int(config.get('AuctionHouseBot.Neutral.Price.Ratio', 200))
        form.items_itemlevel_min.data = int(config.get('AuctionHouseBot.Items.ItemLevel.Min', 0))
        form.items_itemlevel_max.data = int(config.get('AuctionHouseBot.Items.ItemLevel.Max', 0))
        form.items_reqlevel_min.data = int(config.get('AuctionHouseBot.Items.ReqLevel.Min', 0))
        form.items_reqlevel_max.data = int(config.get('AuctionHouseBot.Items.ReqLevel.Max', 0))
        form.items_reqskill_min.data = int(config.get('AuctionHouseBot.Items.ReqSkill.Min', 0))
        form.items_reqskill_max.data = int(config.get('AuctionHouseBot.Items.ReqSkill.Max', 0))
        form.items_amount_grey.data = int(config.get('AuctionHouseBot.Items.Amount.Grey', 0))
        form.items_amount_white.data = int(config.get('AuctionHouseBot.Items.Amount.White', 2000))
        form.items_amount_green.data = int(config.get('AuctionHouseBot.Items.Amount.Green', 2500))
        form.items_amount_blue.data = int(config.get('AuctionHouseBot.Items.Amount.Blue', 1500))
        form.items_amount_purple.data = int(config.get('AuctionHouseBot.Items.Amount.Purple', 1000))
        form.items_amount_orange.data = int(config.get('AuctionHouseBot.Items.Amount.Orange', 0))
        form.items_amount_yellow.data = int(config.get('AuctionHouseBot.Items.Amount.Yellow', 0))
        form.class_consumable.data = int(config.get('AuctionHouseBot.Class.Consumable', 6))
        form.class_container.data = int(config.get('AuctionHouseBot.Class.Container', 4))
        form.class_weapon.data = int(config.get('AuctionHouseBot.Class.Weapon', 8))
        form.class_gem.data = int(config.get('AuctionHouseBot.Class.Gem', 3))
        form.class_armor.data = int(config.get('AuctionHouseBot.Class.Armor', 8))
        form.class_reagent.data = int(config.get('AuctionHouseBot.Class.Reagent', 1))
        form.class_projectile.data = int(config.get('AuctionHouseBot.Class.Projectile', 2))
        form.class_tradegood.data = int(config.get('AuctionHouseBot.Class.TradeGood', 10))
        form.class_generic.data = int(config.get('AuctionHouseBot.Class.Generic', 1))
        form.class_recipe.data = int(config.get('AuctionHouseBot.Class.Recipe', 6))
        form.class_quiver.data = int(config.get('AuctionHouseBot.Class.Quiver', 1))
        form.class_quest.data = int(config.get('AuctionHouseBot.Class.Quest', 1))
        form.class_key.data = int(config.get('AuctionHouseBot.Class.Key', 1))
        form.class_misc.data = int(config.get('AuctionHouseBot.Class.Misc', 5))
        form.class_glyph.data = int(config.get('AuctionHouseBot.Class.Glyph', 3))
        form.class_misc_mount_reqlevel_min.data = int(config.get('AuctionHouseBot.Class.Misc.Mount.ReqLevel.Min', 0))
        form.class_misc_mount_reqlevel_max.data = int(config.get('AuctionHouseBot.Class.Misc.Mount.ReqLevel.Max', 0))
        form.class_misc_mount_reqskill_min.data = int(config.get('AuctionHouseBot.Class.Misc.Mount.ReqSkill.Min', 0))
        form.class_misc_mount_reqskill_max.data = int(config.get('AuctionHouseBot.Class.Misc.Mount.ReqSkill.Max', 0))
        form.class_glyph_reqlevel_min.data = int(config.get('AuctionHouseBot.Class.Glyph.ReqLevel.Min', 0))
        form.class_glyph_reqlevel_max.data = int(config.get('AuctionHouseBot.Class.Glyph.ReqLevel.Max', 0))
        form.class_glyph_itemlevel_min.data = int(config.get('AuctionHouseBot.Class.Glyph.ItemLevel.Min', 0))
        form.class_glyph_itemlevel_max.data = int(config.get('AuctionHouseBot.Class.Glyph.ItemLevel.Max', 0))
        form.class_tradegood_itemlevel_min.data = int(config.get('AuctionHouseBot.Class.TradeGood.ItemLevel.Min', 0))
        form.class_tradegood_itemlevel_max.data = int(config.get('AuctionHouseBot.Class.TradeGood.ItemLevel.Max', 0))
        form.class_container_itemlevel_min.data = int(config.get('AuctionHouseBot.Class.Container.ItemLevel.Min', 0))
        form.class_container_itemlevel_max.data = int(config.get('AuctionHouseBot.Class.Container.ItemLevel.Max', 0))
        form.force_include_items.data = config.get('AuctionHouseBot.forceIncludeItems', '').strip('"')
        form.force_exclude_items.data = config.get('AuctionHouseBot.forceExcludeItems', '').strip('"')
        form.buyer_enabled.data = bool(int(config.get('AuctionHouseBot.Buyer.Enabled', 0)))
        form.buyer_debug.data = bool(int(config.get('AuctionHouseBot.DEBUG.Buyer', 0)))
        form.buyer_alliance_enabled.data = bool(int(config.get('AuctionHouseBot.Buyer.Alliance.Enabled', 1)))
        form.buyer_horde_enabled.data = bool(int(config.get('AuctionHouseBot.Buyer.Horde.Enabled', 1)))
        form.buyer_neutral_enabled.data = bool(int(config.get('AuctionHouseBot.Buyer.Neutral.Enabled', 1)))
        form.buyer_buyprice.data = bool(int(config.get('AuctionHouseBot.Buyer.BuyPrice', 0)))
        form.buyer_recheck_interval.data = int(config.get('AuctionHouseBot.Buyer.Recheck.Interval', 20))
        form.buyer_alliance_chance_ratio.data = int(config.get('AuctionHouseBot.Buyer.Alliance.Chance.Ratio', 3))
        form.buyer_horde_chance_ratio.data = int(config.get('AuctionHouseBot.Buyer.Horde.Chance.Ratio', 3))
        form.buyer_neutral_chance_ratio.data = int(config.get('AuctionHouseBot.Buyer.Neutral.Chance.Ratio', 3))


    return render_template('configuration.html', form=form)

def read_config():
    config = {}
    if os.path.exists('ahbot.conf'):
        with open('ahbot.conf') as f:
            for line in f:
                line = line.strip()
                if not line.startswith(('ConfVersion','AuctionHouseBot.')):
                    continue
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    else:
        # set default values if config file doesn't exist
        config['AuctionHouseBot.CharacterName'] = '\"\"'
        config['AuctionHouseBot.Seller.Enabled'] = 0
        config['AuctionHouseBot.DEBUG.Seller'] = 0
        config['AuctionHouseBot.Alliance.Items.Amount.Ratio'] = 100
        config['AuctionHouseBot.Horde.Items.Amount.Ratio'] = 100
        config['AuctionHouseBot.Neutral.Items.Amount.Ratio'] = 100
        config['AuctionHouseBot.MinTime'] = 1
        config['AuctionHouseBot.MaxTime'] = 72
        config['AuctionHouseBot.Items.Vendor'] = 0
        config['AuctionHouseBot.Items.Loot'] = 1
        config['AuctionHouseBot.Items.Misc'] = 0
        config['AuctionHouseBot.Bind.No'] = 1
        config['AuctionHouseBot.Bind.Pickup'] = 0
        config['AuctionHouseBot.Bind.Equip'] = 1
        config['AuctionHouseBot.Bind.Use'] = 1
        config['AuctionHouseBot.Bind.Quest'] = 0
        config['AuctionHouseBot.LockBox.Enabled'] = 0
        config['AuctionHouseBot.ItemsPerCycle.Boost'] = 75
        config['AuctionHouseBot.ItemsPerCycle.Normal'] = 20
        config['AuctionHouseBot.BuyPrice.Seller'] = 1
        config['AuctionHouseBot.Alliance.Price.Ratio'] = 200
        config['AuctionHouseBot.Horde.Price.Ratio'] = 200
        config['AuctionHouseBot.Neutral.Price.Ratio'] = 200
        config['AuctionHouseBot.Items.ItemLevel.Min'] = 0
        config['AuctionHouseBot.Items.ItemLevel.Max'] = 0
        config['AuctionHouseBot.Items.ReqLevel.Min'] = 0
        config['AuctionHouseBot.Items.ReqLevel.Max'] = 0
        config['AuctionHouseBot.Items.ReqSkill.Min'] = 0
        config['AuctionHouseBot.Items.ReqSkill.Max'] = 0
        config['AuctionHouseBot.Items.Amount.Grey'] = 0
        config['AuctionHouseBot.Items.Amount.White'] = 2000
        config['AuctionHouseBot.Items.Amount.Green'] = 2500
        config['AuctionHouseBot.Items.Amount.Blue'] = 1500
        config['AuctionHouseBot.Items.Amount.Purple'] = 1000
        config['AuctionHouseBot.Items.Amount.Orange'] = 0
        config['AuctionHouseBot.Items.Amount.Yellow'] = 0
        config['AuctionHouseBot.Class.Consumable'] = 6
        config['AuctionHouseBot.Class.Container'] = 4
        config['AuctionHouseBot.Class.Weapon'] = 8
        config['AuctionHouseBot.Class.Gem'] = 3
        config['AuctionHouseBot.Class.Armor'] = 8
        config['AuctionHouseBot.Class.Reagent'] = 1
        config['AuctionHouseBot.Class.Projectile'] = 2
        config['AuctionHouseBot.Class.TradeGood'] = 10
        config['AuctionHouseBot.Class.Generic'] = 1
        config['AuctionHouseBot.Class.Recipe'] = 6
        config['AuctionHouseBot.Class.Quiver'] = 1
        config['AuctionHouseBot.Class.Quest'] = 1
        config['AuctionHouseBot.Class.Key'] = 1
        config['AuctionHouseBot.Class.Misc'] = 5
        config['AuctionHouseBot.Class.Glyph'] = 3
        config['AuctionHouseBot.Class.Misc.Mount.ReqLevel.Min'] = 0
        config['AuctionHouseBot.Class.Misc.Mount.ReqLevel.Max'] = 0
        config['AuctionHouseBot.Class.Misc.Mount.ReqSkill.Min'] = 0
        config['AuctionHouseBot.Class.Misc.Mount.ReqSkill.Max'] = 0
        config['AuctionHouseBot.Class.Glyph.ReqLevel.Min'] = 0
        config['AuctionHouseBot.Class.Glyph.ReqLevel.Max'] = 0
        config['AuctionHouseBot.Class.Glyph.ItemLevel.Min'] = 0
        config['AuctionHouseBot.Class.Glyph.ItemLevel.Max'] = 0
        config['AuctionHouseBot.Class.TradeGood.ItemLevel.Min'] = 0
        config['AuctionHouseBot.Class.TradeGood.ItemLevel.Max'] = 0
        config['AuctionHouseBot.Class.Container.ItemLevel.Min'] = 0
        config['AuctionHouseBot.Class.Container.ItemLevel.Max'] = 0
        config['AuctionHouseBot.forceIncludeItems'] = "\"\""
        config['AuctionHouseBot.forceExcludeItems'] = "\"\""
        config['AuctionHouseBot.Buyer.Enabled'] = 0
        config['AuctionHouseBot.DEBUG.Buyer'] = 0
        config['AuctionHouseBot.Buyer.Alliance.Enabled'] = 1
        config['AuctionHouseBot.Buyer.Horde.Enabled'] = 1
        config['AuctionHouseBot.Buyer.Neutral.Enabled'] = 1
        config['AuctionHouseBot.Buyer.BuyPrice'] = 0
        config['AuctionHouseBot.Buyer.Recheck.Interval'] = 20
        config['AuctionHouseBot.Buyer.Alliance.Chance.Ratio'] = 3
        config['AuctionHouseBot.Buyer.Horde.Chance.Ratio'] = 3
        config['AuctionHouseBot.Buyer.Neutral.Chance.Ratio'] = 3

    return config

def write_config(config):
    with open('ahbot.conf', 'w') as f:
        f.write(conf_header)
        if config.get('ConfVersion') is None:
            confVersion = 2010102201
        else:
            confVersion = config.get('ConfVersion')
        f.write(f"[AhbotConf]\nConfVersion={confVersion}")
        f.write(conf_documentation_1)
        for key, value in config.items():
            if key != "ConfVersion" :
                if not "Buyer" in key:
                    f.write(f'{key} = {value}\n')
        f.write(conf_documentation_2)
        for key, value in config.items():
            if "Buyer" in key:
                f.write(f'{key} = {value}\n')
    flash('success', 'Config saved successfully.')


class AHBotConfigForm(FlaskForm):
    character_name = StringField('Character Name')
    seller_enabled = BooleanField('Seller Enabled')
    seller_debug = BooleanField('Seller Debug')
    alliance_ratio = IntegerField('Alliance Ratio', validators=[NumberRange(min=0, max=100)])
    horde_ratio = IntegerField('Horde Ratio', validators=[NumberRange(min=0, max=100)])
    neutral_ratio = IntegerField('Neutral Ratio', validators=[NumberRange(min=0, max=100)])
    mintime = IntegerField('MinTime', validators=[NumberRange(min=0)])
    maxtime = IntegerField('MaxTime', validators=[NumberRange(min=0)])
    items_vendor = BooleanField('Items Vendor')
    items_loot = BooleanField('Items Loot')
    items_misc = BooleanField('Items Misc')
    bind_no = BooleanField('Bind No')
    bind_pickup = BooleanField('Bind Pickup')
    bind_equip = BooleanField('Bind Equip')
    bind_use = BooleanField('Bind Use')
    bind_quest = BooleanField('Bind Quest')
    lockbox_enabled = BooleanField('Lockbox Enabled')
    itemspercycle_boost = IntegerField('ItemsPerCycle Boost', validators=[NumberRange(min=0)])
    itemspercycle_normal = IntegerField('ItemsPerCycle Normal', validators=[NumberRange(min=0)])
    buyprice_seller = BooleanField('BuyPrice Seller')
    alliance_price_ratio = IntegerField('Alliance Price Ratio', validators=[NumberRange(min=0)])
    horde_price_ratio = IntegerField('Horde Price Ratio', validators=[NumberRange(min=0)])
    neutral_price_ratio = IntegerField('Neutral Price Ratio', validators=[NumberRange(min=0)])
    items_itemlevel_min = IntegerField('Items ItemLevel Minimum', validators=[NumberRange(min=0)])
    items_itemlevel_max = IntegerField('Items ItemLevel Maximum', validators=[NumberRange(min=0)])
    items_reqlevel_min =IntegerField('Items Req Level Minimum', validators=[NumberRange(min=0)])
    items_reqlevel_max =IntegerField('Items Req Level Maximum', validators=[NumberRange(min=0)])
    items_reqskill_min =IntegerField('Items Req Skill Minimum', validators=[NumberRange(min=0)])
    items_reqskill_max =IntegerField('Items Req Skill Maximum', validators=[NumberRange(min=0)])
    items_amount_grey = IntegerField('Items Amount - Grey', validators=[NumberRange(min=0)])
    items_amount_white = IntegerField('Items Amount - White', validators=[NumberRange(min=0)])
    items_amount_green = IntegerField('Items Amount - Green', validators=[NumberRange(min=0)])
    items_amount_blue = IntegerField('Items Amount - Blue', validators=[NumberRange(min=0)])
    items_amount_purple = IntegerField('Items Amount - Purple', validators=[NumberRange(min=0)])
    items_amount_orange = IntegerField('Items Amount - Orange', validators=[NumberRange(min=0)])
    items_amount_yellow = IntegerField('Items Amount - Yellow', validators=[NumberRange(min=0)])
    class_consumable = IntegerField('Consumable Class', validators=[NumberRange(min=0, max=10)])
    class_container = IntegerField('Container Class', validators=[NumberRange(min=0, max=10)])
    class_weapon = IntegerField('Weapon Class', validators=[NumberRange(min=0, max=10)])
    class_gem = IntegerField('Gem Class', validators=[NumberRange(min=0, max=10)])
    class_armor = IntegerField('Armor Class', validators=[NumberRange(min=0, max=10)])
    class_reagent = IntegerField('Reagent Class', validators=[NumberRange(min=0, max=10)])
    class_projectile = IntegerField('Projectile Class', validators=[NumberRange(min=0, max=10)])
    class_tradegood = IntegerField('Tradegood Class', validators=[NumberRange(min=0, max=10)])
    class_generic = IntegerField('Generic Class', validators=[NumberRange(min=0, max=10)])
    class_recipe = IntegerField('Recipe Class', validators=[NumberRange(min=0, max=10)])
    class_quiver = IntegerField('Quiver Class', validators=[NumberRange(min=0, max=10)])
    class_quest = IntegerField('Quest Class', validators=[NumberRange(min=0, max=10)])
    class_key = IntegerField('Key Class', validators=[NumberRange(min=0, max=10)])
    class_misc = IntegerField('Misc Class', validators=[NumberRange(min=0, max=10)])
    class_glyph = IntegerField('Glyph Class', validators=[NumberRange(min=0, max=10)])
    class_misc_mount_reqlevel_min = IntegerField('Mount Reqlevel Min', validators=[NumberRange(min=0)])
    class_misc_mount_reqlevel_max = IntegerField('Mount Reqlevel Max', validators=[NumberRange(min=0)])
    class_misc_mount_reqskill_min = IntegerField('Mount Reqskill Min', validators=[NumberRange(min=0)])
    class_misc_mount_reqskill_max = IntegerField('Mount Reqskill Max', validators=[NumberRange(min=0)])
    class_glyph_reqlevel_min = IntegerField('Glyph Reqlevel Min', validators=[NumberRange(min=0)])
    class_glyph_reqlevel_max = IntegerField('Glyph Reqlevel Max', validators=[NumberRange(min=0)])
    class_glyph_itemlevel_min = IntegerField('Glyph Itemlevel Min', validators=[NumberRange(min=0)])
    class_glyph_itemlevel_max = IntegerField('Glyph Itemlevel Max', validators=[NumberRange(min=0)])
    class_tradegood_itemlevel_min = IntegerField('Tradegood Itemlevel Min', validators=[NumberRange(min=0)])
    class_tradegood_itemlevel_max = IntegerField('Tradegood Itemlevel Max', validators=[NumberRange(min=0)])
    class_container_itemlevel_min = IntegerField('Container Itemlevel Min', validators=[NumberRange(min=0)])
    class_container_itemlevel_max = IntegerField('Container Itemlevel Max', validators=[NumberRange(min=0)])
    force_include_items = StringField('Force Include Items')
    force_exclude_items = StringField('Force Exclude Items')
    buyer_enabled = BooleanField('Buyer Enabled')
    buyer_debug = BooleanField('Buyer Debug')
    buyer_alliance_enabled = BooleanField('Buyer Alliance Enabled')
    buyer_horde_enabled = BooleanField('Buyer Horde Enabled')
    buyer_neutral_enabled = BooleanField('Buyer Neutral Enabled')
    buyer_buyprice = BooleanField('Buyer Buy Price')
    buyer_recheck_interval = IntegerField('Buyer Recheck Interval', validators=[NumberRange(min=0)])
    buyer_alliance_chance_ratio = IntegerField('Buyer Alliance Chance Ratio', validators=[NumberRange(min=0, max=100)])
    buyer_horde_chance_ratio = IntegerField('Buyer Horde Chance Ratio', validators=[NumberRange(min=0, max=100)])
    buyer_neutral_chance_ratio = IntegerField('Buyer Neutral Chance Ratio', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Save')


conf_header = '''################################################################################
# Auction house bot configuration                                              #
################################################################################

'''

conf_documentation_1 = '''

################################################################################
# AUCTION HOUSE BOT SETTINGS
#
#    AuctionHouseBot.CharacterName
#        The name of the character that the bot will use to auction
#        items in the Alliance, Horde and neutral auction houses.
#    Default "" (No owner)
#
#    AuctionHouseBot.Seller.Enabled
#        Enable or disable sales functionality
#    Default 0 (Disabled)
#
#    AuctionHouseBot.DEBUG.Seller
#        Enable or disable sales debug mode
#    Default 0 (Disabled)
#
#    AuctionHouseBot.Alliance.Items.Amount.Ratio
#        Enable or disable sales on Alliance auction houses
#    Default 100 (Enabled with 100% of items)
#
#    AuctionHouseBot.Horde.Items.Amount.Ratio
#        Enable or disable sales on Horde auction houses
#    Default 100 (Enabled with 100% of items)
#
#    AuctionHouseBot.Neutral.Items.Amount.Ratio
#        Enable or disable sales on neutral auction houses
#    Default 100 (Enabled with 100% of items)
#
#    AuctionHouseBot.MinTime
#        Minimum time for new auctions
#    Default 1 (Hour)
#
#    AuctionHouseBot.MaxTime
#        Maximum time for new auctions
#    Default 72 (Hours)
#
#    AuctionHouseBot.Items.Vendor
#        Offer items sold by vendors as auctions
#    Default 0
#
#    AuctionHouseBot.Items.Loot
#        Offer lootable/fishable items as auctions
#    Default 1
#
#    AuctionHouseBot.Items.Misc
#        Offer miscellaneous items as auctions (not recommended)
#    Default 0
#
#    AuctionHouseBot.Bind.*
#        Indicates which bonding types can be put up for auction
#            No     - Items that don't bind            Default 1 (Allowed)
#            Pickup - Items that bind on pickup        Default 0 (Not Allowed)
#            Equip  - Items that bind on equip         Default 1 (Allowed)
#            Use    - Items that bind on use           Default 1 (Allowed)
#            Quest  - Quest Items                      Default 0 (Not Allowed)
#
#    AuctionHouseBot.LockBox.Enabled
#        Enable or disable sales of lock boxes
#    Default 0 (Disabled)
#
#    AuctionHouseBot.ItemsPerCycle.Boost
#        Uses to define how many auctions to add per cycle in an uninitialized
#        auction table.
#    Default 75
#
#    AuctionHouseBot.ItemsPerCycle.Normal
#        Uses to define how many auctions to add per cycle in an initialized
#        auction table.
#    Default 20
#
#    AuctionHouseBot.BuyPrice.Seller
#        Enable or disable the use of BuyPrice or SellPrice to determine bid
#        pricing
#    Default 1 (use SellPrice)
#
#    AuctionHouseBot.Alliance.Price.Ratio
#        Defines the price ratio for auctions on the Alliance auction houses
#    Default 200
#
#    AuctionHouseBot.Horde.Price.Ratio
#        Defines the price ratio for auctions on the Horde auction houses
#    Default 200
#
#    AuctionHouseBot.Neutral.Price.Ratio
#        Defines the price ratio for auctions on the neutral auction houses
#    Default 200
#
#    AuctionHouseBot.Items.ItemLevel.*
#        Enable or disable listing items below/above this item level
#    Default 0 (Disabled)
#
#    AuctionHouseBot.Items.ReqLevel.*
#        Enable or disable listing items below/above this required level
#    Default 0 (Disabled)
#
#    AuctionHouseBot.Items.ReqSkill.*
#        Enable or disable listing items below/above this skill level
#    Default 0 (Disabled)
#
#    AuctionHouseBot.Items.Amount.*
#        Defines the amount of auctions to be created for each item quality
#        Values will be adjusted using faction specific settings (if specified)
#    Default 0, 2000, 2500, 1500, 1000, 0, 0
#            (grey, white, green, blue, purple, orange, yellow)
#
#    AuctionHouseBot.Class.*
#        Defines which item classes can be put up for auction. See pre-defined
#        classes in ItemClass.dbc.
#        These value are preference values, maximum is 10, minimum is 0.
#    Default 6,4,8,3,8,1,2,10,1,6,1,1,1,5,3
#
#
# ITEM FINE TUNING
#    The following are useful for limiting what character levels can benefit
#    from the auction house.
#
#    AuctionHouseBot.Class.Misc.Mount.ReqLevel.*
#        Enable or disable listing mounts below/above this required level
#    Default 0
#
#    AuctionHouseBot.Class.Misc.Mount.ReqSkill.*
#        Enable or disable listing mounts below/above this skill level
#    Default 0
#
#    AuctionHouseBot.Class.Glyph.ReqLevel.*
#        Enable or disable listing glyphs below/above this required level
#    Default 0
#
#    AuctionHouseBot.Class.Glyph.ItemLevel.*
#        Enable or disable listing glyphs below/above this item level
#    Default 0
#
#    AuctionHouseBot.Class.TradeGood.ItemLevel.*
#        Enable or disable listing trade good items below/above this item level
#    Default 0
#
#    AuctionHouseBot.Class.Container.ItemLevel.*
#        Enable or disable listing containers below/above this item level
#    Default 0
#
#    AuctionHouseBot.forceIncludeItems
#        Allows to include items which would normally be ignored by filter
#        settings.
#        List of ids with delimiter ','
#    Default ""
#
#    AuctionHouseBot.forceExcludeItems
#        Allows to exclude items which would normally be included by filter
#        settings.
#        List of ids with delimiter ','
#        Example "21878,27774,27811,28117,28122,43949" (this removes zzOld items)
#    Default ""
#
################################################################################
'''

conf_documentation_2 = '''
################################################################################
# Buyer configuration
#
#    AuctionHouseBot.Buyer.Enabled
#        Enable or disable buyer mode
#    Default 0 (Disabled)
#
#    AuctionHouseBot.DEBUG.Buyer
#        Enable or disable buyer debug mode
#    Default 0 (Disabled)
#
#    AuctionHouseBot.Buyer.FACTION.Enabled
#        Enable or disable buyer mode for a specific faction
#
#    AuctionHouseBot.Buyer.BuyPrice
#        Enable or disable the use of BuyPrice or SellPrice to determine bid
#        pricing
#    Default 0 (use SellPrice)
#
#    AuctionHouseBot.Buyer.Recheck.Interval
#        This specifies the time interval (in minute) between evaluations of
#        identical items.
#        The lower the value is, the higher the chance for an item to be bought
#    Default 20 (20min.)
#
#    AuctionHouseBot.Buyer.FACTION.Chance.Ratio
#       Determines the chance for buying an item.
#    Default 3 (literally 1 chance by 3)
#
################################################################################
'''