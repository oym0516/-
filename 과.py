import os
import hashlib

def file_hash(path, chunk_size=8192):
    """파일 내용을 SHA-256 해시로 변환 (대용량 파일도 안전)"""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def list_files(dir_path):
    """디렉토리 안의 '파일'만 반환 (하위 디렉토리 제외)"""
    return sorted(
        name for name in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, name))
    )


def compare_dirs(dir1, dir2):
    # 1) 존재 여부 확인
    for d in (dir1, dir2):
        if not os.path.isdir(d):
            print(f"[오류] '{d}' 디렉토리가 존재하지 않습니다.")
            return False

    files1 = list_files(dir1)
    files2 = list_files(dir2)

    # 2) 파일 개수 비교
    print(f"\n[1단계] 파일 개수 비교")
    print(f"  {dir1}: {len(files1)}개")
    print(f"  {dir2}: {len(files2)}개")
    if len(files1) != len(files2):
        print("  → 파일 개수가 다릅니다.\n결과: 두 디렉토리는 서로 다릅니다.")
        return False
    print("  → 파일 개수 동일 ✓")

    # 3) 파일 이름 비교
    print(f"\n[2단계] 파일 이름 비교")
    if files1 != files2:
        only1 = set(files1) - set(files2)
        only2 = set(files2) - set(files1)
        if only1: print(f"  {dir1}에만 있음: {only1}")
        if only2: print(f"  {dir2}에만 있음: {only2}")
        print("결과: 두 디렉토리는 서로 다릅니다.")
        return False
    print("  → 파일 이름 모두 동일 ✓")

    # 4) 크기 및 내용 비교
    print(f"\n[3단계] 각 파일의 크기·내용 비교")
    all_same = True
    for name in files1:
        p1 = os.path.join(dir1, name)
        p2 = os.path.join(dir2, name)

        size1, size2 = os.path.getsize(p1), os.path.getsize(p2)
        if size1 != size2:
            print(f"  [✗] {name}: 크기 다름 ({size1} vs {size2} bytes)")
            all_same = False
            continue

        if file_hash(p1) != file_hash(p2):
            print(f"  [✗] {name}: 크기 같음({size1} bytes)지만 내용 다름")
            all_same = False
        else:
            print(f"  [✓] {name}: 동일 ({size1} bytes)")

    print("\n" + "=" * 40)
    if all_same:
        print("결과: 두 디렉토리는 완전히 동일합니다. ✅")
    else:
        print("결과: 두 디렉토리는 서로 다릅니다. ❌")
    return all_same


if __name__ == "__main__":
    d1 = input("첫 번째 디렉토리 이름: ").strip()
    d2 = input("두 번째 디렉토리 이름: ").strip()
    compare_dirs(d1, d2)
