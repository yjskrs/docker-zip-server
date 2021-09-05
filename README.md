# Docker Zip Server

Docker image for hosting webpages from zip files on an apache server.

Uses ubuntu server image as its base and has php installed.

## Usage

To set up, copy the zip files to `public_html/kits`.

Then run the following commands:

```
sudo docker build -t <tag-name> .
sudo docker run -dp <local-port>:80 <tag-name>
```

Your zip files will be hosted on `localhost:<local-port>` in a few moments.
