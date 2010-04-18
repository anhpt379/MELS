
/*
 * Copyright (C) Igor Sysoev
 */


#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <nginx.h>


static ngx_int_t ngx_http_send_error_page(ngx_http_request_t *r,
    ngx_http_err_page_t *err_page);
static ngx_int_t ngx_http_send_special_response(ngx_http_request_t *r,
    ngx_http_core_loc_conf_t *clcf, ngx_uint_t err);
static ngx_int_t ngx_http_send_refresh(ngx_http_request_t *r);


static u_char ngx_http_error_full_tail[] =
"" CRLF
;


static u_char ngx_http_error_tail[] =
"" CRLF
;


static u_char ngx_http_msie_stub[] =
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
"<!-- The padding to disable MSIE's friendly error page -->" CRLF
;


static u_char ngx_http_msie_refresh_head[] =
"";


static u_char ngx_http_msie_refresh_tail[] =
"" CRLF;


static char ngx_http_error_301_page[] =
"<error status_code=\"301\" description=\"Moved Permanently\"/>" CRLF
;


static char ngx_http_error_302_page[] =
"<error status_code=\"302\" description=\"Found\"/>" CRLF
;


static char ngx_http_error_400_page[] =
"<error status_code=\"400\" description=\"Yêu cầu không hợp lệ\"/>" CRLF
;


static char ngx_http_error_401_page[] =
"<error status_code=\"401\" description=\"Authorization Required\"/>" CRLF
;


static char ngx_http_error_402_page[] =
"<error status_code=\"402\" description=\"Payment Required\"/>" CRLF
;


static char ngx_http_error_403_page[] =
"<error status_code=\"403\" description=\"Forbidden\"/>" CRLF
;


static char ngx_http_error_404_page[] =
"<error status_code=\"404\" description=\"Not Found\"/>" CRLF
;


static char ngx_http_error_405_page[] =
"<error status_code=\"405\" description=\"Not Allowed\"/>" CRLF
;


static char ngx_http_error_406_page[] =
"<error status_code=\"406\" description=\"Not Acceptable\"/>" CRLF
;


static char ngx_http_error_408_page[] =
"<error status_code=\"408\" description=\"Request Time-out\"/>" CRLF
;


static char ngx_http_error_409_page[] =
"<error status_code=\"409\" description=\"Conflict\"/>" CRLF
;


static char ngx_http_error_410_page[] =
"<error status_code=\"410\" description=\"Gone\"/>" CRLF
;


static char ngx_http_error_411_page[] =
"<error status_code=\"411\" description=\"Length Required\"/>" CRLF
;


static char ngx_http_error_412_page[] =
"<error status_code=\"412\" description=\"Precondition Failed\"/>" CRLF
;


static char ngx_http_error_413_page[] =
"<error status_code=\"413\" description=\"Request Entity Too Large\"/>" CRLF
;


static char ngx_http_error_414_page[] =
"<error status_code=\"414\" description=\"Request-URI Too Large\"/>" CRLF
;


static char ngx_http_error_415_page[] =
"<error status_code=\"415\" description=\"Unsupported Media Type\"/>" CRLF
;


static char ngx_http_error_416_page[] =
"<error status_code=\"416\" description=\"Requested Range Not Satisfiable\"/>" CRLF
;


static char ngx_http_error_495_page[] =
"" CRLF
;


static char ngx_http_error_496_page[] =
"" CRLF
;


static char ngx_http_error_497_page[] =
"" CRLF
;


static char ngx_http_error_500_page[] =
"<error status_code=\"500\" description=\"Hệ thống gặp phải một lỗi chưa rõ nguyên nhân. Vui lòng báo lại cho bộ phận quản trị khi gặp lỗi này.\"/>" CRLF
;


static char ngx_http_error_501_page[] =
"<error status_code=\"501\" description=\"Method Not Implemented\"/>" CRLF
;


static char ngx_http_error_502_page[] =
"<error status_code=\"502\" description=\"Hệ thống đang được nâng cấp\"/>" CRLF
;


static char ngx_http_error_503_page[] =
"<error status_code=\"503\" description=\"Hệ thống đang quá tải\"/>" CRLF
;


static char ngx_http_error_504_page[] =
"<error status_code=\"504\" description=\"Gateway Time-out\"/>" CRLF
;


static char ngx_http_error_507_page[] =
"" CRLF
;


static ngx_str_t ngx_http_error_pages[] = {

    ngx_null_string,                     /* 201, 204 */

#define NGX_HTTP_LAST_LEVEL_200  202
#define NGX_HTTP_LEVEL_200       (NGX_HTTP_LAST_LEVEL_200 - 201)

    /* ngx_null_string, */               /* 300 */
    ngx_string(ngx_http_error_301_page),
    ngx_string(ngx_http_error_302_page),
    ngx_null_string,                     /* 303 */

#define NGX_HTTP_LAST_LEVEL_300  304
#define NGX_HTTP_LEVEL_300       (NGX_HTTP_LAST_LEVEL_300 - 301)

    ngx_string(ngx_http_error_400_page),
    ngx_string(ngx_http_error_401_page),
    ngx_string(ngx_http_error_402_page),
    ngx_string(ngx_http_error_403_page),
    ngx_string(ngx_http_error_404_page),
    ngx_string(ngx_http_error_405_page),
    ngx_string(ngx_http_error_406_page),
    ngx_null_string,                     /* 407 */
    ngx_string(ngx_http_error_408_page),
    ngx_string(ngx_http_error_409_page),
    ngx_string(ngx_http_error_410_page),
    ngx_string(ngx_http_error_411_page),
    ngx_string(ngx_http_error_412_page),
    ngx_string(ngx_http_error_413_page),
    ngx_string(ngx_http_error_414_page),
    ngx_string(ngx_http_error_415_page),
    ngx_string(ngx_http_error_416_page),

#define NGX_HTTP_LAST_LEVEL_400  417
#define NGX_HTTP_LEVEL_400       (NGX_HTTP_LAST_LEVEL_400 - 400)

    ngx_string(ngx_http_error_495_page), /* 495, https certificate error */
    ngx_string(ngx_http_error_496_page), /* 496, https no certificate */
    ngx_string(ngx_http_error_497_page), /* 497, http to https */
    ngx_string(ngx_http_error_404_page), /* 498, canceled */
    ngx_null_string,                     /* 499, client has closed connection */

    ngx_string(ngx_http_error_500_page),
    ngx_string(ngx_http_error_501_page),
    ngx_string(ngx_http_error_502_page),
    ngx_string(ngx_http_error_503_page),
    ngx_string(ngx_http_error_504_page),
    ngx_null_string,                     /* 505 */
    ngx_null_string,                     /* 506 */
    ngx_string(ngx_http_error_507_page)

#define NGX_HTTP_LAST_LEVEL_500  508

};


static ngx_str_t  ngx_http_get_name = { 3, (u_char *) "GET " };


ngx_int_t
ngx_http_special_response_handler(ngx_http_request_t *r, ngx_int_t error)
{
    ngx_uint_t                 i, err;
    ngx_http_err_page_t       *err_page;
    ngx_http_core_loc_conf_t  *clcf;

    ngx_log_debug3(NGX_LOG_DEBUG_HTTP, r->connection->log, 0,
                   "http special response: %d, \"%V?%V\"",
                   error, &r->uri, &r->args);

    r->err_status = error;

    if (r->keepalive) {
        switch (error) {
            case NGX_HTTP_BAD_REQUEST:
            case NGX_HTTP_REQUEST_ENTITY_TOO_LARGE:
            case NGX_HTTP_REQUEST_URI_TOO_LARGE:
            case NGX_HTTP_TO_HTTPS:
            case NGX_HTTPS_CERT_ERROR:
            case NGX_HTTPS_NO_CERT:
            case NGX_HTTP_INTERNAL_SERVER_ERROR:
                r->keepalive = 0;
        }
    }

    if (r->lingering_close == 1) {
        switch (error) {
            case NGX_HTTP_BAD_REQUEST:
            case NGX_HTTP_TO_HTTPS:
            case NGX_HTTPS_CERT_ERROR:
            case NGX_HTTPS_NO_CERT:
                r->lingering_close = 0;
        }
    }

    r->headers_out.content_type.len = 0;

    clcf = ngx_http_get_module_loc_conf(r, ngx_http_core_module);

    if (!r->error_page && clcf->error_pages && r->uri_changes != 0) {

        if (clcf->recursive_error_pages == 0) {
            r->error_page = 1;
        }

        err_page = clcf->error_pages->elts;

        for (i = 0; i < clcf->error_pages->nelts; i++) {
            if (err_page[i].status == error) {
                return ngx_http_send_error_page(r, &err_page[i]);
            }
        }
    }

    r->expect_tested = 1;

    if (ngx_http_discard_request_body(r) != NGX_OK) {
        error = NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    if (clcf->msie_refresh
        && r->headers_in.msie
        && (error == NGX_HTTP_MOVED_PERMANENTLY
            || error == NGX_HTTP_MOVED_TEMPORARILY))
    {
        return ngx_http_send_refresh(r);
    }

    if (error == NGX_HTTP_CREATED) {
        /* 201 */
        err = 0;
        r->header_only = 1;

    } else if (error == NGX_HTTP_NO_CONTENT) {
        /* 204 */
        err = 0;

    } else if (error >= NGX_HTTP_MOVED_PERMANENTLY
               && error < NGX_HTTP_LAST_LEVEL_300)
    {
        /* 3XX */
        err = error - NGX_HTTP_MOVED_PERMANENTLY + NGX_HTTP_LEVEL_200;

    } else if (error >= NGX_HTTP_BAD_REQUEST
               && error < NGX_HTTP_LAST_LEVEL_400)
    {
        /* 4XX */
        err = error - NGX_HTTP_BAD_REQUEST + NGX_HTTP_LEVEL_200
                                           + NGX_HTTP_LEVEL_300;

    } else if (error >= NGX_HTTP_OWN_CODES
               && error < NGX_HTTP_LAST_LEVEL_500)
    {
        /* 49X, 5XX */
        err = error - NGX_HTTP_OWN_CODES + NGX_HTTP_LEVEL_200
                                         + NGX_HTTP_LEVEL_300
                                         + NGX_HTTP_LEVEL_400;
        switch (error) {
            case NGX_HTTP_TO_HTTPS:
            case NGX_HTTPS_CERT_ERROR:
            case NGX_HTTPS_NO_CERT:
                r->err_status = NGX_HTTP_BAD_REQUEST;
                break;
        }

    } else {
        /* unknown code, zero body */
        err = 0;
    }

    return ngx_http_send_special_response(r, clcf, err);
}


ngx_int_t
ngx_http_filter_finalize_request(ngx_http_request_t *r, ngx_module_t *m,
    ngx_int_t error)
{
    void       *ctx;
    ngx_int_t   rc;

    ngx_http_clean_header(r);

    ctx = NULL;

    if (m) {
        ctx = r->ctx[m->ctx_index];
    }

    /* clear the modules contexts */
    ngx_memzero(r->ctx, sizeof(void *) * ngx_http_max_module);

    if (m) {
        r->ctx[m->ctx_index] = ctx;
    }

    r->filter_finalize = 1;

    rc = ngx_http_special_response_handler(r, error);

    /* NGX_ERROR resets any pending data */

    switch (rc) {

    case NGX_OK:
    case NGX_DONE:
        return NGX_ERROR;

    default:
        return rc;
    }
}


void
ngx_http_clean_header(ngx_http_request_t *r)
{
    ngx_memzero(&r->headers_out.status,
                sizeof(ngx_http_headers_out_t)
                    - offsetof(ngx_http_headers_out_t, status));

    r->headers_out.headers.part.nelts = 0;
    r->headers_out.headers.part.next = NULL;
    r->headers_out.headers.last = &r->headers_out.headers.part;

    r->headers_out.content_length_n = -1;
    r->headers_out.last_modified_time = -1;
}


static ngx_int_t
ngx_http_send_error_page(ngx_http_request_t *r, ngx_http_err_page_t *err_page)
{
    ngx_int_t                  overwrite;
    ngx_str_t                  uri, args;
    ngx_table_elt_t           *location;
    ngx_http_core_loc_conf_t  *clcf;

    overwrite = err_page->overwrite;

    if (overwrite && overwrite != NGX_HTTP_OK) {
        r->expect_tested = 1;
    }

    r->err_status = overwrite;

    r->zero_in_uri = 0;

    if (ngx_http_complex_value(r, &err_page->value, &uri) != NGX_OK) {
        return NGX_ERROR;
    }

    if (uri.data[0] == '/') {

        if (err_page->value.lengths) {
            ngx_http_split_args(r, &uri, &args);

        } else {
            args = err_page->args;
        }

        if (r->method != NGX_HTTP_HEAD) {
            r->method = NGX_HTTP_GET;
            r->method_name = ngx_http_get_name;
        }

        return ngx_http_internal_redirect(r, &uri, &args);
    }

    if (uri.data[0] == '@') {
        return ngx_http_named_location(r, &uri);
    }

    location = ngx_list_push(&r->headers_out.headers);

    if (location == NULL) {
        return NGX_ERROR;
    }

    r->err_status = NGX_HTTP_MOVED_TEMPORARILY;

    location->hash = 1;
    location->key.len = sizeof("Location") - 1;
    location->key.data = (u_char *) "Location";
    location->value = uri;

    r->headers_out.location = location;

    clcf = ngx_http_get_module_loc_conf(r, ngx_http_core_module);

    if (clcf->msie_refresh && r->headers_in.msie) {
        return ngx_http_send_refresh(r);
    }

    return ngx_http_send_special_response(r, clcf, NGX_HTTP_MOVED_TEMPORARILY
                                                   - NGX_HTTP_MOVED_PERMANENTLY
                                                   + NGX_HTTP_LEVEL_200);
}


static ngx_int_t
ngx_http_send_special_response(ngx_http_request_t *r,
    ngx_http_core_loc_conf_t *clcf, ngx_uint_t err)
{
    u_char       *tail;
    size_t        len;
    ngx_int_t     rc;
    ngx_buf_t    *b;
    ngx_uint_t    msie_padding;
    ngx_chain_t   out[3];

    if (clcf->server_tokens) {
        len = sizeof(ngx_http_error_full_tail) - 1;
        tail = ngx_http_error_full_tail;

    } else {
        len = sizeof(ngx_http_error_tail) - 1;
        tail = ngx_http_error_tail;
    }

    msie_padding = 0;

    if (!r->zero_body) {
        if (ngx_http_error_pages[err].len) {
            r->headers_out.content_length_n = ngx_http_error_pages[err].len
                                              + len;
            if (clcf->msie_padding
                && r->headers_in.msie
                && r->http_version >= NGX_HTTP_VERSION_10
                && err >= NGX_HTTP_LEVEL_300)
            {
                r->headers_out.content_length_n +=
                                                sizeof(ngx_http_msie_stub) - 1;
                msie_padding = 1;
            }

            r->headers_out.content_type_len = sizeof("text/xml") - 1;
            r->headers_out.content_type.len = sizeof("text/xml") - 1;
            r->headers_out.content_type.data = (u_char *) "text/xml";
            r->headers_out.content_type_lowcase = NULL;

        } else {
            r->headers_out.content_length_n = -1;
        }

    } else {
        r->headers_out.content_length_n = 0;
        err = 0;
    }

    if (r->headers_out.content_length) {
        r->headers_out.content_length->hash = 0;
        r->headers_out.content_length = NULL;
    }

    ngx_http_clear_accept_ranges(r);
    ngx_http_clear_last_modified(r);

    rc = ngx_http_send_header(r);

    if (rc == NGX_ERROR || r->header_only) {
        return rc;
    }

    if (ngx_http_error_pages[err].len == 0) {
        return NGX_OK;
    }

    b = ngx_calloc_buf(r->pool);
    if (b == NULL) {
        return NGX_ERROR;
    }

    b->memory = 1;
    b->pos = ngx_http_error_pages[err].data;
    b->last = ngx_http_error_pages[err].data + ngx_http_error_pages[err].len;

    out[0].buf = b;
    out[0].next = &out[1];

    b = ngx_calloc_buf(r->pool);
    if (b == NULL) {
        return NGX_ERROR;
    }

    b->memory = 1;

    b->pos = tail;
    b->last = tail + len;

    out[1].buf = b;
    out[1].next = NULL;

    if (msie_padding) {
        b = ngx_calloc_buf(r->pool);
        if (b == NULL) {
            return NGX_ERROR;
        }

        b->memory = 1;
        b->pos = ngx_http_msie_stub;
        b->last = ngx_http_msie_stub + sizeof(ngx_http_msie_stub) - 1;

        out[1].next = &out[2];
        out[2].buf = b;
        out[2].next = NULL;
    }

    if (r == r->main) {
        b->last_buf = 1;
    }

    b->last_in_chain = 1;

    return ngx_http_output_filter(r, &out[0]);
}


static ngx_int_t
ngx_http_send_refresh(ngx_http_request_t *r)
{
    u_char       *p, *location;
    size_t        len, size;
    uintptr_t     escape;
    ngx_int_t     rc;
    ngx_buf_t    *b;
    ngx_chain_t   out;

    len = r->headers_out.location->value.len;
    location = r->headers_out.location->value.data;

    escape = 2 * ngx_escape_uri(NULL, location, len, NGX_ESCAPE_REFRESH);

    size = sizeof(ngx_http_msie_refresh_head) - 1
           + escape + len
           + sizeof(ngx_http_msie_refresh_tail) - 1;

    r->err_status = NGX_HTTP_OK;

    r->headers_out.content_type_len = sizeof("text/xml") - 1;
    r->headers_out.content_type.len = sizeof("text/xml") - 1;
    r->headers_out.content_type.data = (u_char *) "text/xml";
    r->headers_out.content_type_lowcase = NULL;

    r->headers_out.location->hash = 0;
    r->headers_out.location = NULL;

    r->headers_out.content_length_n = size;

    if (r->headers_out.content_length) {
        r->headers_out.content_length->hash = 0;
        r->headers_out.content_length = NULL;
    }

    ngx_http_clear_accept_ranges(r);
    ngx_http_clear_last_modified(r);

    rc = ngx_http_send_header(r);

    if (rc == NGX_ERROR || r->header_only) {
        return rc;
    }

    b = ngx_create_temp_buf(r->pool, size);
    if (b == NULL) {
        return NGX_ERROR;
    }

    p = ngx_cpymem(b->pos, ngx_http_msie_refresh_head,
                   sizeof(ngx_http_msie_refresh_head) - 1);

    if (escape == 0) {
        p = ngx_cpymem(p, location, len);

    } else {
        p = (u_char *) ngx_escape_uri(p, location, len, NGX_ESCAPE_REFRESH);
    }

    b->last = ngx_cpymem(p, ngx_http_msie_refresh_tail,
                         sizeof(ngx_http_msie_refresh_tail) - 1);

    b->last_buf = 1;
    b->last_in_chain = 1;

    out.buf = b;
    out.next = NULL;

    return ngx_http_output_filter(r, &out);
}
