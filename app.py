from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


# =========================
# Google 인증
# =========================
@app.route("/googlefe08a61fd67fcbae.html")
def google_verification():
    return send_from_directory(".", "googlefe08a61fd67fcbae.html")


# =========================
# 사이트맵
# =========================
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml")


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
# PC 전기요금 계산기
# =========================
@app.route("/electricity", methods=["GET", "POST"])
def electricity():

    result = None

    if request.method == "POST":

        try:
            power = float(request.form["power"])
            hours = float(request.form["hours"])
            days = float(request.form["days"])
            price = float(request.form["price"])

            if power <= 0:
                result = "소비전력은 0보다 커야 합니다."

            elif hours < 0 or hours > 24:
                result = "하루 사용시간은 0~24시간 사이로 입력해주세요."

            elif days < 0 or days > 31:
                result = "사용일수는 0~31일 사이로 입력해주세요."

            elif price < 0:
                result = "전력량 요금은 0 이상이어야 합니다."

            else:

                # W → kW
                power_kw = power / 1000

                # 예상 월간 전력 사용량
                monthly_kwh = power_kw * hours * days

                # 예상 전기요금
                monthly_cost = monthly_kwh * price

                result = (
                    f"⚡ <strong>예상 전기요금</strong><br><br>"
                    f"월간 예상 사용량: "
                    f"<strong>{monthly_kwh:.2f} kWh</strong><br>"
                    f"예상 전기요금: "
                    f"<strong>{monthly_cost:,.0f}원</strong>"
                )

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "electricity.html",
        result=result
    )


# =========================
# 인터넷 속도 계산기
# =========================
@app.route("/speed", methods=["GET", "POST"])
def speed():

    result = None

    if request.method == "POST":

        try:
            file_size = float(request.form["file_size"])
            hours = float(request.form["hours"])
            minutes = float(request.form["minutes"])

            if file_size <= 0:
                result = "파일 크기는 0보다 커야 합니다."

            elif hours < 0:
                result = "시간은 0 이상이어야 합니다."

            elif minutes < 0 or minutes >= 60:
                result = "분은 0~59 사이로 입력해주세요."

            elif hours == 0 and minutes == 0:
                result = "목표 시간은 0보다 커야 합니다."

            else:

                # 목표 시간을 초로 변환
                total_seconds = (hours * 3600) + (minutes * 60)

                # GB → MB
                file_mb = file_size * 1024

                # 필요한 MB/s
                required_mb_per_second = file_mb / total_seconds

                # MB/s → Mbps
                required_mbps = required_mb_per_second * 8

                if required_mbps >= 1000:
                    speed_result = f"{required_mbps / 1000:.2f} Gbps"
                else:
                    speed_result = f"{required_mbps:,.0f} Mbps"

                result = (
                    "🚀 <strong>필요한 인터넷 속도</strong><br><br>"
                    f"파일 크기: <strong>{file_size:g} GB</strong><br>"
                    f"목표 시간: <strong>{int(hours)}시간 "
                    f"{int(minutes)}분</strong><br><br>"
                    f"필요한 속도: <strong>{speed_result}</strong>"
                )

        except ValueError:
            result = "숫자를 올바르게 입력해주세요."

    return render_template(
        "speed.html",
        result=result
    )


# =========================
# FPS 프레임타임 표
# =========================
@app.route("/fps-table")
def fps_table():
    return render_template("fps_table.html")


@app.route("/reaction")
def reaction():
    return render_template("reaction.html")


# =========================
# 서버 실행
# =========================
if __name__ == "__main__":
    app.run(debug=True)
