//
//  DrinkCollectionViewCell.h
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import "Drink.h"
#import "MBProgressHUD.h"

@protocol ServeDrinkDelegate <NSObject>

-(void) serveDrinkWithId: (int) drinkId;

@end

@interface DrinkCollectionViewCell : UICollectionViewCell

@property (strong, nonatomic) IBOutlet UILabel * drinkName;
@property (strong, nonatomic) IBOutlet UITextView * drinkDescription;
@property (strong, nonatomic) Drink * drink;
@property (weak,nonatomic) id <ServeDrinkDelegate> serveDrinkDelegate;
@property (strong, nonatomic) IBOutlet UIButton *pourButton;


- (IBAction)pourDrink:(id)sender;

- (void) populateUIwithDatafrom:(Drink *)aDrink;

@property (strong, nonatomic) IBOutlet UIImageView *drinkImageView;

@end
