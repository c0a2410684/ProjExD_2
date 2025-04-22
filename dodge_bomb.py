import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True

    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0,HEIGHT)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bl_img = pg.Surface((1100, 650))
    pg.draw.rect(bl_img, (0, 0, 0), (0, 0, 1100,650))
    bl_img.set_alpha(200)
    bl_rct = bl_img.get_rect()
    bl_rct.center = 550, 325
    moji = pg.font.Font(None,80)
    kokaton = pg.image.load("fig/8.png")
    txt = moji.render("Game Over", True, (255, 255, 255))

    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    
    def gameover(screen: pg.Surface) -> None:
        """
        ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表
示し，泣いているこうかとん画像を貼り付ける関数
        """

        height: int = 280  #こうかとんと文字の高さ
        screen.blit(bl_img, bl_rct)
        screen.blit(txt, [400, height])
        screen.blit(kokaton, [330, height])
        screen.blit(kokaton, [730, height])

        pg.display.update()
        time.sleep(5)
    
    # bb_accs = [a for a in range(1, 11)]
    # for r in range(1, 11):
    #     bb_img = pg.surface((20*r, 20*r))
    #     pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)

    # def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    #     bb_accs = tuple(bb_accs)
    #     bb_img = tuple(bb_img)
        
    kk_img2 = pg.transform.flip(kk_img, True, False)
    def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
        jisyo = {
            (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
            (-5,-5):pg.transform.rotozoom(kk_img, -45, 1.0),
            (-5,5):pg.transform.rotozoom(kk_img, 45, 1.0),
            (0,-5):pg.transform.rotozoom(kk_img2, 90, 1.0),
            (5,-5):pg.transform.rotozoom(kk_img2, 45, 1.0),
            (5,0):pg.transform.rotozoom(kk_img2, 0, 1.0),
            (5,5):pg.transform.rotozoom(kk_img2, -45, 1.0),
            (0,5):pg.transform.rotozoom(kk_img2, -90, 1.0),
        }
        for k, v in jisyo.items():
            if sum_mv == k:
                return v
        else:
            return pg.transform.rotozoom(kk_img, 0, 1.0)
            
        
        



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)  #関数の実装
            print(gameover.__doc__)  #docstring
            print("game over")
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(5,0)}
        for key, (x,y) in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += x
                sum_mv[1] += y

        # bb_imgs, bb_accs = init_bb_imgs()
        # avx = vx*bb_accs[min(tmr//500, 9)]
        # bb_img = bb_imgs[min(tmr//500, 9)]
        kk_imgs = get_kk_img(sum_mv)
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #画面内に戻す
        screen.blit(kk_imgs, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1

        screen.blit(bb_img, bb_rct)  #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
