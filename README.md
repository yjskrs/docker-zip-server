# Docker Zip Server

Docker image for hosting webpages from zip files on an apache server.

Uses ubuntu server image as its base and has php installed.

## Usage

To set up, create an empty directory `public_html/kits` and copy the zip files into it.

Then run the following commands:

```
sudo docker build -t <tag-name> .
sudo docker run -dp <local-port>:80 <tag-name>
```

Your zip files will be hosted on `localhost:<local-port>` in a few moments (can take quite a while if the zip files are large).
