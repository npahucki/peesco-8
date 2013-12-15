//
//  DrinkCollectionViewCell.h
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DrinkCollectionViewCell : UICollectionViewCell

@property (strong, nonatomic) IBOutlet UILabel *drinkName;
@property (strong, nonatomic) IBOutlet UITextView *drinkDescription;


- (IBAction)pourDrink:(id)sender;

@end
