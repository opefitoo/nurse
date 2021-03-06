from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'invoices.views.home', name='home'),
    # url(r'^invoices/', include('invoices.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
     # include the lookup urls
    (r'^admin/lookups/', include(ajax_select_urls)),
    #url(r'admin/invoices/invoiceitem/pdf_report/(?P<invoice_item>\w+)/$', views.pdf_report, name='pdf_report')

)
