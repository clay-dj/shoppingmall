# Generated by Django 2.2.5 on 2022-04-12 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('logo', models.ImageField(upload_to='', verbose_name='Logo图片')),
                ('first_letter', models.CharField(max_length=1, verbose_name='品牌首字母')),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'db_table': 'tb_brand',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='goods.GoodsCategory', verbose_name='父类别')),
            ],
            options={
                'verbose_name': '商品类别',
                'verbose_name_plural': '商品类别',
                'db_table': 'tb_goods_category',
            },
        ),
        migrations.CreateModel(
            name='GoodsChannelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=20, verbose_name='频道组名')),
            ],
            options={
                'verbose_name': '商品频道组',
                'verbose_name_plural': '商品频道组',
                'db_table': 'tb_channel_group',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('caption', models.CharField(max_length=100, verbose_name='副标题')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='单价')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='进价')),
                ('market_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='市场价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('comments', models.IntegerField(default=0, verbose_name='评价数')),
                ('is_launched', models.BooleanField(default=True, verbose_name='是否上架销售')),
                ('default_image', models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='默认图片')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.GoodsCategory', verbose_name='从属类别')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'db_table': 'tb_sku',
            },
        ),
        migrations.CreateModel(
            name='SPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('comments', models.IntegerField(default=0, verbose_name='评价数')),
                ('desc_detail', models.TextField(default='', verbose_name='详细介绍')),
                ('desc_pack', models.TextField(default='', verbose_name='包装信息')),
                ('desc_service', models.TextField(default='', verbose_name='售后服务')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Brand', verbose_name='品牌')),
                ('category1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat1_spu', to='goods.GoodsCategory', verbose_name='一级类别')),
                ('category2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat2_spu', to='goods.GoodsCategory', verbose_name='二级类别')),
                ('category3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat3_spu', to='goods.GoodsCategory', verbose_name='三级类别')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'tb_spu',
            },
        ),
        migrations.CreateModel(
            name='SPUSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=20, verbose_name='规格名称')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='goods.SPU', verbose_name='商品SPU')),
            ],
            options={
                'verbose_name': '商品SPU规格',
                'verbose_name_plural': '商品SPU规格',
                'db_table': 'tb_spu_specification',
            },
        ),
        migrations.CreateModel(
            name='SpecificationOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('value', models.CharField(max_length=20, verbose_name='选项值')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='goods.SPUSpecification', verbose_name='规格')),
            ],
            options={
                'verbose_name': '规格选项',
                'verbose_name_plural': '规格选项',
                'db_table': 'tb_specification_option',
            },
        ),
        migrations.CreateModel(
            name='SKUSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.SpecificationOption', verbose_name='规格值')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='goods.SKU', verbose_name='sku')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.SPUSpecification', verbose_name='规格名称')),
            ],
            options={
                'verbose_name': 'SKU规格',
                'verbose_name_plural': 'SKU规格',
                'db_table': 'tb_sku_specification',
            },
        ),
        migrations.CreateModel(
            name='SKUImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('image', models.ImageField(upload_to='', verbose_name='图片')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.SKU', verbose_name='sku')),
            ],
            options={
                'verbose_name': 'SKU图片',
                'verbose_name_plural': 'SKU图片',
                'db_table': 'tb_sku_image',
            },
        ),
        migrations.AddField(
            model_name='sku',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.SPU', verbose_name='商品'),
        ),
        migrations.CreateModel(
            name='GoodsChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('url', models.CharField(max_length=50, verbose_name='频道页面链接')),
                ('sequence', models.IntegerField(verbose_name='组内顺序')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='顶级商品类别')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsChannelGroup', verbose_name='频道组名')),
            ],
            options={
                'verbose_name': '商品频道',
                'verbose_name_plural': '商品频道',
                'db_table': 'tb_goods_channel',
            },
        ),
    ]
