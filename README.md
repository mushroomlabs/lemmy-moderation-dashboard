### Lemmy Admin - A web based application to manage operations on Lemmy instances

## Overview

A Python/Django application that can interface with a Lemmy instance,
designed to help moderators and instance admins to carry out their
tasks more efficiently. Unlike the other frontends which can only
interact with the Lemmy backend through its API, this tool also can
have access to the Lemmy database, which provides more flexibility and
allows different use-cases outside of the scope defined by the API. Examples:

 - Moderators do not need to be registered users of the instance.
 - Automated tasks (Moderation bots) can be centrally managed and use
   of data that is not available on the API.
 - Django Admin permission systems permit more granular control over
   access. You can have, e.g, moderators being able to carry out
   admin-level tasks only for actions that affect users from specific
   communities.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)



## Usage

The included docker-compose file was created to help during
development. It already defines a lemmy instance that can be used as
the mirror and you need to provide the config.hjson and nginx.conf
(TODO: add sample files). Once these are in place, you should be able
to start the services.

1. Start the Fediverser application using Docker Compose:

   ```bash
   docker-compose up -d
   ```

1. The site will be available on `http://localhost:8000`, and the instance should be accessible on `http://localhost:8888`.

1. In order to test federation, you will need to serve this on the public web, from a real domain and serving via HTTPS. For this, the easiest solution I've found at the moment would be run something like Cloudflare Tunnel connected to `https://localhost:8888`.


## License

This project is licensed under the [GNU Affero General Public License (AGPL)](LICENSE-AGPL-3.0). Feel free to use, modify, and distribute it according to the terms of the license.
