from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route("/googlefe08a61fd67fcbae.html")
def google_verification():
    return send_from_directory(".", "googlefe08a61fd67fcbae.html")


# =========================
# 홈
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# 다운로드 시간 계산기
# =========================
@app.route("/download", methods=["GET", "POST"])
def download():

    result = None

    if request.method == "POST":

        try:
            file_size = float(request.form["size"])
            speed = float(request.form["speed"])

            if file_size <= 0 or speed <= 0:
                result = "파일 크기와 인터넷 속도는 0보다 커야 합니다."

            else:
                # GB → MB
                file_mb = file_size * 1024

                # Mbps → MB/s
                speed_mb = speed / 8

                # 다운로드 시간(초)
                seconds = file_mb / speed_mb

                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)

                if hours > 0:
                    result = f"{hours}시간 {minutes}분 {secs}초"

                elif minutes > 0:
                    result = f"{minutes}분 {secs}초"

                else:
                    result = f"{secs}초"

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "download.html",
        result=result
    )


# =========================
# 저장공간 단위 변환기
# =========================
@app.route("/storage", methods=["GET", "POST"])
def storage():

    result = None

    if request.method == "POST":

        try:
            value = float(request.form["value"])
            unit = request.form["unit"]

            if value < 0:
                result = "용량은 0 이상이어야 합니다."

            else:

                # 모든 값을 KB로 변환
                if unit == "KB":
                    kb = value

                elif unit == "MB":
                    kb = value * 1024

                elif unit == "GB":
                    kb = value * 1024 * 1024

                elif unit == "TB":
                    kb = value * 1024 * 1024 * 1024

                else:
                    kb = value

                mb = kb / 1024
                gb = mb / 1024
                tb = gb / 1024

                result = (
                    f"<strong>{kb:,.2f} KB</strong><br>"
                    f"{mb:,.2f} MB<br>"
                    f"{gb:,.2f} GB<br>"
                    f"{tb:,.2f} TB"
                )

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "storage.html",
        result=result
    )


# =========================
# 게임 설치 공간 계산기
# =========================
@app.route("/game-storage", methods=["GET", "POST"])
def game_storage():

    result = None

    if request.method == "POST":

        try:
            free_space = float(request.form["free_space"])
            game_size = float(request.form["game_size"])
            update_size = float(request.form["update_size"])

            if free_space < 0 or game_size < 0 or update_size < 0:

                result = "용량은 0 이상이어야 합니다."

            else:

                required_space = game_size + update_size
                remaining_space = free_space - required_space

                if remaining_space >= 0:

                    result = (
                        "✅ <strong>설치 가능합니다!</strong><br><br>"
                        f"필요한 공간: {required_space:.2f} GB<br>"
                        f"설치 후 예상 여유 공간: "
                        f"{remaining_space:.2f} GB"
                    )

                else:

                    result = (
                        "❌ <strong>설치 공간이 부족합니다.</strong><br><br>"
                        f"필요한 공간: {required_space:.2f} GB<br>"
                        f"추가로 필요한 공간: "
                        f"{-remaining_space:.2f} GB"
                    )

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "storage_game.html",
        result=result
    )


# =========================
# FPS 프레임타임 계산기
# =========================
@app.route("/fps", methods=["GET", "POST"])
def fps():

    result = None

    if request.method == "POST":

        try:
            fps_value = float(request.form["fps"])

            if fps_value <= 0:

                result = "FPS는 0보다 커야 합니다."

            else:

                # 프레임타임 = 1000 / FPS
                frame_time = 1000 / fps_value

                result = (
                    f"<strong>{fps_value:g} FPS</strong><br><br>"
                    f"프레임타임: "
                    f"<strong>{frame_time:.2f} ms</strong>"
                )

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "fps.html",
        result=result
    )


# =========================
# 서버 실행
# =========================
if __name__ == "__main__":
    app.run(debug=True)
