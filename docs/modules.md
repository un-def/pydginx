# Modules

## [ngx_core_module](https://nginx.org/en/docs/ngx_core_module.html)

<details>
  <summary>Directives</summary>

  * [x] accept_mutex
  * [ ] accept_mutex_delay
  * [x] daemon
  * [ ] debug_connection
  * [ ] debug_points
  * [ ] env
  * [ ] error_log
  * [x] events
  * [ ] include
  * [ ] load_module
  * [ ] lock_file
  * [ ] master_process
  * [ ] multi_accept
  * [ ] pcre_jit
  * [x] pid
  * [ ] ssl_engine
  * [ ] thread_pool
  * [ ] timer_resolution
  * [ ] use
  * [ ] user
  * [ ] worker_aio_requests
  * [x] worker_connections
  * [ ] worker_cpu_affinity
  * [ ] worker_priority
  * [ ] worker_processes
  * [ ] worker_rlimit_core
  * [ ] worker_rlimit_nofile
  * [ ] worker_shutdown_timeout
  * [ ] working_directory
</details>

## [ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html)

<details>
  <summary>Directives</summary>

  * [ ] absolute_redirect
  * [ ] aio
  * [ ] aio_write
  * [ ] alias
  * [ ] auth_delay
  * [ ] chunked_transfer_encoding
  * [ ] client_body_buffer_size
  * [ ] client_body_in_file_only
  * [ ] client_body_in_single_buffer
  * [ ] client_body_temp_path
  * [ ] client_body_timeout
  * [ ] client_header_buffer_size
  * [ ] client_header_timeout
  * [ ] client_max_body_size
  * [ ] connection_pool_size
  * [ ] default_type
  * [ ] directio
  * [ ] directio_alignment
  * [ ] disable_symlinks
  * [ ] error_page
  * [ ] etag
  * [ ] http
  * [ ] if_modified_since
  * [ ] ignore_invalid_headers
  * [ ] internal
  * [ ] keepalive_disable
  * [ ] keepalive_requests
  * [ ] keepalive_time
  * [ ] keepalive_timeout
  * [ ] large_client_header_buffers
  * [ ] limit_except
  * [ ] limit_rate
  * [ ] limit_rate_after
  * [ ] lingering_close
  * [ ] lingering_time
  * [ ] lingering_timeout
  * [ ] listen
  * [ ] location
  * [ ] log_not_found
  * [ ] log_subrequest
  * [ ] max_ranges
  * [ ] merge_slashes
  * [ ] msie_padding
  * [ ] msie_refresh
  * [ ] open_file_cache
  * [ ] open_file_cache_errors
  * [ ] open_file_cache_min_uses
  * [ ] open_file_cache_valid
  * [ ] output_buffers
  * [ ] port_in_redirect
  * [ ] postpone_output
  * [ ] read_ahead
  * [ ] recursive_error_pages
  * [ ] request_pool_size
  * [ ] reset_timedout_connection
  * [ ] resolver
  * [ ] resolver_timeout
  * [ ] root
  * [ ] satisfy
  * [ ] send_lowat
  * [ ] send_timeout
  * [ ] sendfile
  * [ ] sendfile_max_chunk
  * [ ] server
  * [ ] server_name
  * [ ] server_name_in_redirect
  * [ ] server_names_hash_bucket_size
  * [ ] server_names_hash_max_size
  * [ ] server_tokens
  * [ ] subrequest_output_buffer_size
  * [ ] tcp_nodelay
  * [ ] tcp_nopush
  * [ ] try_files
  * [ ] types
  * [ ] types_hash_bucket_size
  * [ ] types_hash_max_size
  * [ ] underscores_in_headers
  * [ ] variables_hash_bucket_size
  * [ ] variables_hash_max_size
</details>

<details>
  <summary>Variables</summary>

  * [ ] $arg_ *name*
  * [ ] $args
  * [ ] $binary_remote_addr
  * [ ] $body_bytes_sent
  * [ ] $bytes_sent
  * [ ] $connection
  * [ ] $connection_requests
  * [ ] $connection_time
  * [ ] $content_length
  * [ ] $content_type
  * [ ] $cookie_ *name*
  * [ ] $document_root
  * [ ] $document_uri
  * [ ] $host
  * [ ] $hostname
  * [ ] $http_ *name*
  * [ ] $https
  * [ ] $is_args
  * [ ] $limit_rate
  * [ ] $msec
  * [ ] $nginx_version
  * [ ] $pid
  * [ ] $pipe
  * [ ] $proxy_protocol_addr
  * [ ] $proxy_protocol_port
  * [ ] $proxy_protocol_server_addr
  * [ ] $proxy_protocol_server_port
  * [ ] $proxy_protocol_tlv_ *name*
  * [ ] $query_string
  * [ ] $realpath_root
  * [ ] $remote_addr
  * [ ] $remote_port
  * [ ] $remote_user
  * [ ] $request
  * [ ] $request_body
  * [ ] $request_body_file
  * [ ] $request_completion
  * [ ] $request_filename
  * [ ] $request_id
  * [ ] $request_length
  * [ ] $request_method
  * [ ] $request_time
  * [ ] $request_uri
  * [ ] $scheme
  * [ ] $sent_http_ *name*
  * [ ] $sent_trailer_ *name*
  * [ ] $server_addr
  * [ ] $server_name
  * [ ] $server_port
  * [ ] $server_protocol
  * [ ] $status
  * [ ] $tcpinfo_rtt
  * [ ] $tcpinfo_rttvar
  * [ ] $tcpinfo_snd_cwnd
  * [ ] $tcpinfo_rcv_space
  * [ ] $time_iso8601
  * [ ] $time_local
  * [ ] $uri
</details>

## [ngx_http_log_module](https://nginx.org/en/docs/http/ngx_http_log_module.html)

<details>
  <summary>Directives</summary>

  * [ ] access_log
  * [ ] log_format
  * [ ] open_log_file_cache
</details>

<details>
  <summary>Variables</summary>

  * [ ] $bytes_sent
  * [ ] $connection
  * [ ] $connection_requests
  * [ ] $msec
  * [ ] $pipe
  * [ ] $request_length
  * [ ] $request_time
  * [ ] $status
  * [ ] $time_iso8601
  * [ ] $time_local
</details>
