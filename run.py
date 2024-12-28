from flaskblog import createApp

app = createApp()


if __name__ == "__main__":
    try:
    # Your code
        app.run(debug=True)
        # app.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()