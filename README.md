# Zero Trust Network Basics

Studies based in day 51-52 of 100 Days System Design for DevOps and Cloud Engineers.

https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f

Days 51–60: Security and Compliance at Scale

Day 51–52: Implement a zero-trust network architecture in a cloud environment.

## Project Overview

* A Zero Trust Network Architecture (ZTNA) is a security model that shifts the focus from perimeter-based defenses to a more granular, identity-centric approach. Traditional security models operate on the assumption that everything inside the network is trustworthy, while zero trust assumes that threats can originate from both inside and outside the network. In a zero-trust model, every request is treated as if it originates from an open network, meaning no entity (whether human or machine) is trusted by default.

### The core principles of zero trust include:

* Verify every request: Authentication and authorization are required for every interaction, regardless of the network's origin.
* Least privilege access: Users and services are only given the minimum level of access needed.
* Assume breach: Act as if your environment is already compromised, and build in systems to detect and mitigate damage.
* Key Components of Zero Trust in This Project:
* Mutual TLS (mTLS): Every service-to-service communication is encrypted and authenticated, ensuring that both sides of the communication can be trusted.
* Identity-Based Access Control: Access between containers is strictly controlled, ensuring that services can only communicate based on identity and policies.
* Container Isolation: Each service (container) runs in its own isolated environment, minimizing the impact of any potential breach.
* Granular Logging and Monitoring: All network activity is logged and monitored to detect suspicious behavior and respond to potential security incidents quickly.
* In this project, we demonstrate the implementation of Zero Trust principles between two FastAPI-based microservices running in Docker containers. The services communicate with each other using mTLS to ensure encrypted and authenticated communication.

### How This Project Works

* Dockerized FastAPI services: The project contains two FastAPI microservices that are isolated in separate Docker containers.
* mTLS (mutual TLS): Services authenticate each other using certificates, ensuring both ends of the communication are trusted.
* Network Segmentation: The services run in a dedicated Docker network to limit external access and create a secure communication path.
* Zero Trust Security: Each service is treated as untrusted by default. All communication between services is authenticated and encrypted using SSL certificates.

## How to Use

### Prerequisites

* Docker and Docker Compose installed on your system.
* OpenSSL for generating certificates.

### Steps

* Clone the repository:
```
git clone https://github.com/your-repo/zero-trust-network.git
cd zero-trust-network
```

* Generate Certificates: Use OpenSSL to generate the root CA, server certificates, and configure the SAN (Subject Alternative Name) entries for the FastAPI services as described in the documentation.
```
# 1. Generate a Root CA
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt -subj "/CN=rootCA"

# 2. Generate server key and CSR for FastAPI container 1
openssl genrsa -out server1.key 2048
openssl req -new -key server1.key -out server1.csr -subj "/CN=fastapi1.local"

# 3. Generate the server certificate for FastAPI container 1
openssl x509 -req -in server1.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server1.crt -days 500 -sha256

# 4. Repeat for FastAPI container 2
openssl genrsa -out server2.key 2048
openssl req -new -key server2.key -out server2.csr -subj "/CN=fastapi2.local"
openssl x509 -req -in server2.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server2.crt -days 500 -sha256

# 5. Generate client certificates if needed for client authentication
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/CN=client"
openssl x509 -req -in client.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out client.crt -days 500 -sha256
```


```
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt -subj "/C=US/ST=California/L=San Francisco/O=YourCompany/OU=YourDepartment/CN=rootCA"
```

```
vim san.cnf
```

Copy and paste this:
```
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[ dn ]
C = US
ST = California
L = San Francisco
O = YourCompany
OU = YourDepartment
CN = fastapi2

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = fastapi2
DNS.2 = fastapi1
```

Regenerate every time you need:
```
# Generate a new key for fastapi2
openssl genrsa -out server2.key 2048

# Generate a CSR using the new config with SAN
openssl req -new -key server2.key -out server2.csr -config san.cnf

# Sign the certificate using your root CA
openssl x509 -req -in server2.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server2.crt -days 500 -sha256 -extensions req_ext -extfile san.cnf
```

* After generating the certificates, use Docker Compose to run the FastAPI services:
```
docker-compose up
```

* Test Communication: Visit https://localhost:8000/call_container2 to test the communication between the FastAPI services. Both services communicate securely using mutual TLS authentication.

## Author
This project was implemented by [Lucas de Queiroz dos Reis][2]. It is based on the [100 Days System Design for DevOps and Cloud Engineers][1].

[1]: https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f "Medium - Deo Shankar 100 Days"
[2]: https://www.linkedin.com/in/lucas-de-queiroz/ "LinkedIn - Lucas de Queiroz"
