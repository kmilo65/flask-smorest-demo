## Run the Docker container locally with the Flask development server and debugger

If you use this Dockerfile, it doesn't mean you can't run it locally using the Flask development server. You don't have to lose the automatic restarting capabilities, or the Flask debugger.

To run the Docker container locally, you'll have to do this from now on:

 ```
 docker run -dp 5000:5000 -w /app -v "$(pwd):/app" teclado-site-flask sh -c "flask run --host 0.0.0.0"
  ```