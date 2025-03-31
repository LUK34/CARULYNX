import dns.resolver

target_domain = 'youtube.com'
records_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA']

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google Public DNS

for record_type in records_types:
    try:
        answer = resolver.resolve(target_domain, record_type, lifetime=5)
    except dns.resolver.NoAnswer:
        continue
    except dns.resolver.NXDOMAIN:
        print(f"{target_domain} does not exist.")
        break
    except dns.resolver.Timeout:
        print(f"Timeout occurred for record type {record_type}")
        continue
    except Exception as e:
        print(f"Error occurred for record type {record_type}: {e}")
        continue


    print(f'{record_type} records for {target_domain}:')
    for data in answer:
        print(f'{data}')
    print("---------------------------------------------------")